#!/usr/bin/env python3
"""
环境预检与自愈守护 (Environment Sentinel & Self-Healing)

核心功能:
1. 端口冲突检测与自动释放 (3 分钟采样率)
2. 依赖项完整性校验与自动修复
3. 环境变量自动补偿
4. 服务健康检查与自动重启

使用方式:
    python3 env_sentinel.py --start      # 启动守护进程
    python3 env_sentinel.py --status     # 查看状态
    python3 env_sentinel.py --check      # 手动检查一次
"""

import os
import sys
import json
import time
import signal
import logging
import subprocess
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# 配置
CONFIG = {
    "services": {
        "backend": {"port": 8000, "name": "后端 API", "command": "cd backend && python3 -m uvicorn app.main:app --port 8000"},
        "frontend": {"port": 8001, "name": "前端页面", "command": "cd frontend && npm run dev"},
    },
    "check_interval": 180,  # 3 分钟
    "log_dir": "logs",
    "report_dir": "reports",
    "dependencies": {
        "backend": ["fastapi", "uvicorn", "sqlalchemy", "playwright"],
        "frontend": ["react", "antd", "umi"],
    }
}

class EnvironmentSentinel:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.log_dir = self.base_path / "logs"
        self.report_dir = self.base_path / "reports"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.report_dir.mkdir(parents=True, exist_ok=True)
        
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_dir / "sentinel.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        self.running = True
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        self.logger.info("收到停止信号，正在关闭...")
        self.running = False
    
    def check_port(self, port: int) -> Optional[int]:
        """检查端口占用情况，返回占用端口的 PID"""
        try:
            result = subprocess.run(
                f"lsof -i :{port} 2>/dev/null | grep LISTEN | awk '{{print $2}}'",
                shell=True, capture_output=True, text=True
            )
            if result.stdout.strip():
                return int(result.stdout.strip().split('\n')[0])
        except Exception as e:
            self.logger.error(f"检查端口 {port} 失败：{e}")
        return None
    
    def kill_process(self, pid: int, force: bool = False) -> bool:
        """终止进程"""
        try:
            signal_type = signal.SIGKILL if force else signal.SIGTERM
            os.kill(pid, signal_type)
            self.logger.info(f"已终止进程 PID: {pid}")
            return True
        except Exception as e:
            self.logger.error(f"终止进程 {pid} 失败：{e}")
            return False
    
    def check_dependencies(self, service: str) -> Dict:
        """检查依赖完整性"""
        result = {"service": service, "missing": [], "status": "ok"}
        
        if service == "backend":
            # 检查 Python 依赖
            for pkg in CONFIG["dependencies"]["backend"]:
                try:
                    subprocess.run(
                        f"python3 -c 'import {pkg}'",
                        shell=True, capture_output=True, check=True
                    )
                except subprocess.CalledProcessError:
                    result["missing"].append(pkg)
                    result["status"] = "broken"
        
        elif service == "frontend":
            # 检查 node_modules
            node_modules = self.base_path / "frontend" / "node_modules"
            if not node_modules.exists():
                result["missing"].append("node_modules")
                result["status"] = "broken"
        
        return result
    
    def fix_dependencies(self, service: str) -> bool:
        """自动修复依赖"""
        self.logger.info(f"开始修复 {service} 依赖...")
        
        if service == "backend":
            cmd = f"cd {self.base_path}/backend && pip3 install -r requirements.txt --break-system-packages -q"
        elif service == "frontend":
            cmd = f"cd {self.base_path}/frontend && npm install"
        
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.logger.info(f"{service} 依赖修复成功")
                return True
        except Exception as e:
            self.logger.error(f"修复依赖失败：{e}")
        return False
    
    def check_service_health(self, name: str, port: int) -> bool:
        """检查服务健康状态"""
        try:
            result = subprocess.run(
                f"curl -s http://localhost:{port}/health 2>/dev/null",
                shell=True, capture_output=True, text=True, timeout=5
            )
            return result.returncode == 0 and "healthy" in result.stdout
        except:
            return False
    
    def start_service(self, name: str, command: str) -> bool:
        """启动服务"""
        self.logger.info(f"启动服务：{name}")
        try:
            subprocess.Popen(
                command,
                shell=True,
                cwd=str(self.base_path),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(3)
            return True
        except Exception as e:
            self.logger.error(f"启动服务 {name} 失败：{e}")
            return False
    
    def run_check(self) -> Dict:
        """执行一次完整检查"""
        timestamp = datetime.now().isoformat()
        report = {
            "timestamp": timestamp,
            "services": {},
            "actions": [],
            "summary": {"total": 0, "healthy": 0, "fixed": 0, "failed": 0}
        }
        
        for service_name, config in CONFIG["services"].items():
            port = config["port"]
            name = config["name"]
            
            report["summary"]["total"] += 1
            service_status = {
                "name": name,
                "port": port,
                "status": "unknown",
                "issues": []
            }
            
            # 1. 检查端口占用
            pid = self.check_port(port)
            if pid:
                # 检查是否是预期服务
                if not self.check_service_health(name, port):
                    self.logger.warning(f"{name} 端口 {port} 被占用 (PID: {pid})")
                    self.kill_process(pid, force=True)
                    report["actions"].append(f"强制释放 {name} 端口 {port}")
                    service_status["issues"].append(f"端口冲突，已释放 PID {pid}")
            
            # 2. 检查依赖
            dep_check = self.check_dependencies(service_name)
            if dep_check["status"] == "broken":
                self.logger.warning(f"{name} 依赖缺失：{dep_check['missing']}")
                if self.fix_dependencies(service_name):
                    report["actions"].append(f"修复 {name} 依赖")
                    report["summary"]["fixed"] += 1
                    service_status["issues"].append(f"依赖已修复")
                else:
                    service_status["issues"].append(f"依赖修复失败")
                    report["summary"]["failed"] += 1
            
            # 3. 检查服务健康
            if self.check_service_health(name, port):
                service_status["status"] = "healthy"
                report["summary"]["healthy"] += 1
                self.logger.info(f"✅ {name} 运行正常")
            else:
                # 尝试启动服务
                self.logger.warning(f"{name} 未运行，尝试启动...")
                if self.start_service(name, config["command"]):
                    time.sleep(5)
                    if self.check_service_health(name, port):
                        service_status["status"] = "started"
                        report["actions"].append(f"启动 {name}")
                        report["summary"]["fixed"] += 1
                    else:
                        service_status["status"] = "failed"
                        service_status["issues"].append("服务启动失败")
                        report["summary"]["failed"] += 1
                else:
                    service_status["status"] = "down"
                    service_status["issues"].append("服务未运行")
                    report["summary"]["failed"] += 1
            
            report["services"][service_name] = service_status
        
        # 保存报告
        report_file = self.report_dir / f"check_{timestamp.replace(':', '-')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def daemon_loop(self):
        """守护进程主循环"""
        self.logger.info("=" * 50)
        self.logger.info("环境守护进程已启动")
        self.logger.info(f"检查间隔：{CONFIG['check_interval']}秒")
        self.logger.info("=" * 50)
        
        while self.running:
            try:
                report = self.run_check()
                
                # 输出摘要
                summary = report["summary"]
                self.logger.info("-" * 50)
                self.logger.info(f"检查完成：健康={summary['healthy']}/{summary['total']}, "
                               f"修复={summary['fixed']}, 失败={summary['failed']}")
                
                if report["actions"]:
                    self.logger.info("执行操作:")
                    for action in report["actions"]:
                        self.logger.info(f"  - {action}")
                
                # 等待下次检查
                if self.running:
                    time.sleep(CONFIG["check_interval"])
                
            except Exception as e:
                self.logger.error(f"检查循环错误：{e}")
                time.sleep(10)
        
        self.logger.info("守护进程已停止")


def main():
    parser = argparse.ArgumentParser(description="环境预检与自愈守护")
    parser.add_argument("--start", action="store_true", help="启动守护进程")
    parser.add_argument("--status", action="store_true", help="查看服务状态")
    parser.add_argument("--check", action="store_true", help="手动检查一次")
    parser.add_argument("--path", type=str, default="/Users/songyanjie/opentest/00Bank_down/smart-downloader",
                       help="项目根路径")
    
    args = parser.parse_args()
    
    sentinel = EnvironmentSentinel(args.path)
    
    if args.start:
        sentinel.daemon_loop()
    elif args.status:
        print("服务状态检查中...")
        report = sentinel.run_check()
        print(json.dumps(report, indent=2))
    elif args.check:
        print("执行手动检查...")
        report = sentinel.run_check()
        print(f"\n检查完成：健康={report['summary']['healthy']}/{report['summary']['total']}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
