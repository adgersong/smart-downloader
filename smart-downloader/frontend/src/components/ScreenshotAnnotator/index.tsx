import React, { useState, useRef } from 'react';
import { Stage, Layer, Rect, Circle, Text } from 'react-konva';
import { Button, Space } from 'antd';

interface BoundingBox {
  x: number;
  y: number;
  width: number;
  height: number;
  type: string;
}

interface ScreenshotAnnotatorProps {
  imageSrc: string;
  onAnnotate?: (boxes: BoundingBox[]) => void;
}

const ScreenshotAnnotator: React.FC<ScreenshotAnnotatorProps> = ({
  imageSrc,
  onAnnotate,
}) => {
  const [boxes, setBoxes] = useState<BoundingBox[]>([]);
  const [isDrawing, setIsDrawing] = useState(false);
  const [startPos, setStartPos] = useState({ x: 0, y: 0 });
  const [annotationType, setAnnotationType] = useState('click');
  const stageRef = useRef<any>(null);

  const handleMouseDown = (e: any) => {
    const pos = e.target.getStage().getPointerPosition();
    setIsDrawing(true);
    setStartPos(pos);
  };

  const handleMouseMove = (e: any) => {
    if (!isDrawing) return;

    const pos = e.target.getStage().getPointerPosition();
    const width = pos.x - startPos.x;
    const height = pos.y - startPos.y;

    setBoxes((prev) => {
      const newBoxes = [...prev.filter((_, i) => i !== prev.length - 1)];
      newBoxes.push({
        x: startPos.x,
        y: startPos.y,
        width,
        height,
        type: annotationType,
      });
      return newBoxes;
    });
  };

  const handleMouseUp = () => {
    setIsDrawing(false);
    onAnnotate?.(boxes);
  };

  const handleClear = () => {
    setBoxes([]);
    onAnnotate?.([]);
  };

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <Space>
          <Button
            type={annotationType === 'click' ? 'primary' : 'default'}
            onClick={() => setAnnotationType('click')}
          >
            点击
          </Button>
          <Button
            type={annotationType === 'type' ? 'primary' : 'default'}
            onClick={() => setAnnotationType('type')}
          >
            输入
          </Button>
          <Button
            type={annotationType === 'download' ? 'primary' : 'default'}
            onClick={() => setAnnotationType('download')}
          >
            下载
          </Button>
          <Button onClick={handleClear}>清空</Button>
        </Space>
      </div>
      <Stage
        width={800}
        height={600}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        ref={stageRef}
      >
        <Layer>
          {imageSrc && (
            <React.Konva.Image
              image={(() => {
                const img = new window.Image();
                img.src = imageSrc;
                return img;
              })()}
              width={800}
              height={600}
            />
          )}
          {boxes.map((box, i) => (
            <React.Fragment key={i}>
              <Rect
                x={box.x}
                y={box.y}
                width={box.width}
                height={box.height}
                stroke="#0071E3"
                strokeWidth={2}
                dash={[5, 5]}
              />
              <Text
                x={box.x}
                y={box.y - 20}
                text={box.type}
                fontSize={12}
                fill="#0071E3"
              />
            </React.Fragment>
          ))}
        </Layer>
      </Stage>
    </div>
  );
};

export default ScreenshotAnnotator;
