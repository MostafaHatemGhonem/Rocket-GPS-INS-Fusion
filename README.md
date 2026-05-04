# Rocket-GPS-INS-Fusion

مشروع دمج بيانات GPS و INS لتتبع الصواريخ.

## هيكلة المشروع

- `firmware/`: أكواد الأردوينو والمستشعرات (عمر).
- `src/`: أكواد البايثون الأساسية.
    - `kinematics.py`: حسابات INS (مريم).
    - `kalman_filter.py`: مرشح كالمان (تسنيم).
    - `visualizer.py`: الرسم البياني (ألاء).
    - `main.py`: نقطة الإدخال (مصطفى).
- `tests/`: سكريبتات الاختبار (بيانات وهمية).

## البدء بالعمل

1. تثبيت المكتبات المطلوبة:
   ```bash
   pip install -r requirements.txt
   ```
2. تشغيل الكود الأساسي:
   ```bash
   python src/main.py
   ```
