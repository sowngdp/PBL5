from tensorflow.keras.applications import ResNet152V2
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
from tensorflow.keras.models import Model

# Tạo lại kiến trúc mô hình, giả sử bạn có số lượng lớp đầu ra là `NUM_CLASSES`
base_model = ResNet152V2(weights=None, include_top=False, input_shape=(64, 64, 3))
x = base_model.output
x = GlobalAveragePooling2D()(x)
outputs = Dense(62, activation='softmax')(x)
model = Model(inputs=base_model.input, outputs=outputs)

# Tải trọng số đã lưu vào mô hình
model.load_weights('./src/weights/model_weights.weights.h5')

# Biên dịch mô hình
#model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

#model.summary()

# Giả sử `test_images` là mảng NumPy của dữ liệu hình ảnh đã được tiền xử lý
predictions = model.predict(test_images)

# Xử lý `predictions` để lấy thông tin mong muốn
# Ví dụ, lấy chỉ số của lớp có xác suất cao nhất
predicted_classes = np.argmax(predictions, axis=1)

