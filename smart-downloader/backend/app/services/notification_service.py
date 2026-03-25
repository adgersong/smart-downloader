"""
通知服务模块
支持邮件、钉钉、企业微信通知
"""
import httpx
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any, Optional
from loguru import logger


class NotificationService:
    """通知服务"""
    
    def __init__(
        self,
        email_config: Optional[Dict] = None,
        dingtalk_webhook: Optional[str] = None,
        wechat_webhook: Optional[str] = None
    ):
        self.email_config = email_config
        self.dingtalk_webhook = dingtalk_webhook
        self.wechat_webhook = wechat_webhook
    
    async def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        html: bool = False
    ) -> bool:
        """发送邮件通知"""
        if not self.email_config:
            logger.warning("邮件配置缺失，无法发送邮件")
            return False
        
        try:
            msg = MIMEMultipart()
            msg["From"] = self.email_config["from"]
            msg["To"] = to
            msg["Subject"] = subject
            
            msg.attach(MIMEText(body, "html" if html else "plain"))
            
            server = smtplib.SMTP(
                self.email_config["smtp_server"],
                self.email_config["smtp_port"]
            )
            server.starttls()
            server.login(
                self.email_config["username"],
                self.email_config["password"]
            )
            server.send_message(msg)
            server.quit()
            
            logger.info(f"邮件已发送：{to} - {subject}")
            return True
        
        except Exception as e:
            logger.error(f"邮件发送失败：{str(e)}")
            return False
    
    async def send_dingtalk(
        self,
        webhook: Optional[str] = None,
        title: str = "通知",
        text: str = "",
        at_all: bool = False
    ) -> bool:
        """发送钉钉通知"""
        url = webhook or self.dingtalk_webhook
        if not url:
            logger.warning("钉钉 webhook 缺失")
            return False
        
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(
                    url,
                    json={
                        "msgtype": "markdown",
                        "markdown": {
                            "title": title,
                            "text": text
                        },
                        "at": {
                            "isAtAll": at_all
                        }
                    }
                )
                
                result = response.json()
                if result.get("errcode") == 0:
                    logger.info("钉钉通知已发送")
                    return True
                else:
                    logger.error(f"钉钉通知失败：{result}")
                    return False
        
        except Exception as e:
            logger.error(f"钉钉通知异常：{str(e)}")
            return False
    
    async def send_wechat(
        self,
        webhook: Optional[str] = None,
        content: str = ""
    ) -> bool:
        """发送企业微信通知"""
        url = webhook or self.wechat_webhook
        if not url:
            logger.warning("企业微信 webhook 缺失")
            return False
        
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(
                    url,
                    json={
                        "msgtype": "text",
                        "text": {
                            "content": content
                        }
                    }
                )
                
                result = response.json()
                if result.get("errcode") == 0:
                    logger.info("企业微信通知已发送")
                    return True
                else:
                    logger.error(f"企业微信通知失败：{result}")
                    return False
        
        except Exception as e:
            logger.error(f"企业微信通知异常：{str(e)}")
            return False
    
    async def send_task_notification(
        self,
        task_id: int,
        task_name: str,
        status: str,
        recipients: List[str],
        error_message: Optional[str] = None
    ):
        """发送任务通知"""
        if status == "success":
            title = f"✅ 任务完成：{task_name}"
            text = f"**任务执行成功**\n\n- 任务 ID: {task_id}\n- 任务名称：{task_name}\n- 执行时间：{self._now()}"
        else:
            title = f"❌ 任务失败：{task_name}"
            text = f"**任务执行失败**\n\n- 任务 ID: {task_id}\n- 任务名称：{task_name}\n- 错误信息：{error_message}\n- 执行时间：{self._now()}"
        
        # 发送邮件
        for email in recipients:
            await self.send_email(email, title, text.replace("**", ""), html=False)
        
        # 发送钉钉
        await self.send_dingtalk(title=title, text=text)
        
        # 发送企业微信
        await self.send_wechat(content=f"{title}\n{text}")
    
    def _now(self) -> str:
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")


# 全局服务实例
_service = None


def get_notification_service() -> NotificationService:
    """获取全局通知服务实例，使用 Settings 中的配置"""
    global _service
    if _service is None:
        from ..config.settings import Settings
+        settings = Settings()
+        email_cfg = {
+            "from": settings.SMTP_FROM,
+            "smtp_server": settings.SMTP_HOST,
+            "smtp_port": settings.SMTP_PORT,
+            "username": settings.SMTP_USER,
+            "password": settings.SMTP_PASSWORD,
+        } if settings.SMTP_HOST else None
+        _service = NotificationService(
+            email_config=email_cfg,
+            dingtalk_webhook=settings.DINGTALK_WEBHOOK_URL or None,
+            wechat_webhook=settings.WECHAT_WEBHOOK_URL or None,
+        )
+    return _service
