from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.ensemble import RandomForestRegressor
import numpy as np

app = FastAPI()

# 1. Khởi tạo và Train mô hình mẫu (Trong thực tế, bạn sẽ load file .pkl đã train)
# Dữ liệu mẫu (Diện tích, Số phòng ngủ, Mã khu vực) -> Giá nhà
X_train = np.array([[50, 1, 1], [75, 2, 1], [100, 3, 2], [120, 4, 2]])
y_train = np.array([2.5, 3.5, 5.0, 6.2]) # Đơn vị: Tỷ VNĐ

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 2. Định nghĩa cấu trúc dữ liệu nhận từ Back-end/UI
class PropertyData(BaseModel):
    area: float
    bedrooms: int
    location_code: int

# 3. Tạo API Endpoint để dự đoán giá
@app.post("/api/predict-price")
def predict_price(data: PropertyData):
    input_features = np.array([[data.area, data.bedrooms, data.location_code]])
    predicted_price = model.predict(input_features)[0]

    return {
        "status": "success",
        "input": data.dict(),
        "predicted_price_billion_vnd": round(predicted_price, 2)
    }

# Lệnh chạy server (gõ vào terminal): uvicorn ai_service:app --reload