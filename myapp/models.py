from django.db import models
from django.contrib.admin.decorators import display
from django.db.models import Model
from django.db.models.fields.files import ImageField
from django.template.loader import get_template
from django import forms 
from django.utils import timezone
    
     # 2. ຕົວເລືອກແຂວງໃນ ສປປ ລາວ ທັງໝົດ 18 ແຂວງ
PROVINCE_CHOICES = [
    ('ນະຄອນຫຼວງວຽງຈັນ', 'ນະຄອນຫຼວງວຽງຈັນ'),
    ('ຜົ້ງສາລີ', 'ຜົ້ງສາລີ'),
    ('ຫຼວງນ້ຳທາ', 'ຫຼວງນ້ຳທา'),
    ('ອຸດົມໄຊ', 'ອຸດົມໄຊ'),
    ('ບໍ່ແກ້ວ', 'ບໍ່ແກ້ວ'),
    ('ຫຼວງພະບາງ', 'ຫຼວງພະບາງ'),
    ('ຫົວພັນ', 'ຫົວພັນ'),
    ('ໄຊຍະບູລີ', 'ໄຊຍະບູລີ'),
    ('ຊຽງຂວາງ', 'ຊຽງຂວາງ'),
    ('ວຽງຈັນ', 'ວຽງຈັນ'),
    ('ບໍລິຄຳໄຊ', 'ບໍລິຄຳໄຊ'),
    ('ຄຳມ່ວນ', 'ຄຳມ່ວນ'),
    ('ສະຫວັນນະເຂດ', 'ສະຫວັນນະເຂດ'),
    ('ສາລະວັນ', 'ສາລະວັນ'),
    ('ເຊກອງ', 'ເຊກອງ'),
    ('ຈຳປາສັກ', 'ຈຳປາສັກ'),
    ('ອັດຕະປື', 'ອັດຕະປື'),
    ('ໄຊສົມບູນ', 'ໄຊສົມບູນ'),
]

class Subject(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='subject_photos/', blank=True, null=True)
    description = models.TextField(blank=True, null=True, default='')
    Name_eng = models.CharField(blank=True, null=True, default='')
    price = models.CharField(max_length=255, null=True, blank=True, default='')
    is_premium = models.BooleanField(default=False)
    promotion_end_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    GENDER_CHOICES = [
        ('ນາງ', 'ນາງ'),
        ('ທ້າວ', 'ທ້າວ'),
        ('ພຣະ', 'ພຣະ'),
       
    ]

    STATUS = [
        ('unapproved', 'Unapproved'),
        ('approved', 'Approved'),
    ]

    GENDER_CHOICES1 = [
        ('Mr', 'Mr'),
        ('Miss', 'Miss'),
    ]

    STATUS = [
        ('unapproved', 'Unapproved'),
        ('approved', 'Approved'),
    ]

    # Personal Info
    StudentID = models.CharField(max_length=60, blank=True)
    gender_eng = models.CharField(max_length=10, choices=GENDER_CHOICES1)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    name = models.CharField(max_length=60)
    Username_lao= models.CharField(max_length=60)
    name_eng = models.CharField(max_length=60)
    Username_eng= models.CharField(max_length=60)
    age = models.CharField(max_length=10)
    birthday = models.DateField(null=True, blank=True)
    photo = models.ImageField(blank=True, null=True)
    Profile = models.TextField(blank=True, null=True, default='')
    Nationality = models.CharField(max_length=60, blank=True)
    Religion= models.CharField(max_length=60, blank=True)
    Buddhism= models.CharField(max_length=60, blank=True)
    # Contact Info
    email = models.EmailField(max_length=60, unique=True)
    tel = models.CharField(max_length=20)
    province = models.CharField(max_length=60,choices=PROVINCE_CHOICES)
    districts = models.CharField(max_length=60)
    village = models.CharField(max_length=60)
    Current_province = models.CharField(max_length=60,blank=True)
    Current_districts = models.CharField(max_length=60 ,blank=True)
    Current_village = models.CharField(max_length=60,blank=True)
    Mobile_Parents = models.CharField(max_length=60,blank=True)
    # Education & Work
    from_school = models.CharField(max_length=60)
    academic_year = models.CharField(max_length=60)
    semester = models.CharField(max_length=60)
    employee = models.CharField(max_length=100, blank=True)
    subject = models.CharField(max_length=60,blank=True)
    province_school = models.CharField(max_length=60,blank=True)
    districts_school = models.CharField(max_length=60,blank=True)
    village_school = models.CharField(max_length=60,blank=True)
   

    # System Fields
    Other_Skill = models.CharField(max_length=60 ,blank=True)
    Skill = models.CharField(max_length=60 ,blank=True)
    Language = models.CharField(max_length=60 ,blank=True)
    Language1 = models.CharField(max_length=60 ,blank=True)
    Language2 = models.CharField(max_length=60 ,blank=True)
    status = models.CharField(max_length=15, choices=STATUS, default='unapproved')
    registered_at = models.DateTimeField(auto_now_add=True)
    subject_set = models.ManyToManyField(Subject)

    def __str__(self):
        return f'{self.name_lao} (id={self.id})'
    
    
class MyModel(Model):
    my_image_field = ImageField()

    # This is our new field. It renders a preview of the image before and post save.
    @display(description='Preview')
    def my_image_thumbnail(self):
        return get_template('my_image_thumbnail_template.html').render({
            'field_name': 'my_image_field',
            'src': self.my_image_field.url if self.my_image_field else None,
        })



class FormResponse(models.Model):
    PROVINCE_CHOICES3 = [
    ('Vientiane Capital', 'ນະຄອນຫຼວງວຽງຈັນ'),
    ('Phongsaly', 'ຜົ້ງສາລີ'),
    ('Luang Namtha', 'ຫຼວງນ້ຳທາ'),
    ('Oudomxay', 'ອຸດົມໄຊ'),
    ('Bokeo', 'ບໍ່ແກ້ວ'),
    ('Luang Prabang', 'ຫຼວງພະບາງ'),
    ('Huaphan', 'ຫົວພັນ'),
    ('Xayaboury', 'ໄຊຍະບູລີ'),
    ('Xieng Khouang', 'ຊຽງຂວາງ'),
    ('Vientiane', 'ວຽງຈັນ'),
    ('Bolikhamxay', 'ບໍລິຄຳໄຊ'),
    ('Khammouane', 'ຄຳມ່ວນ'),
    ('Savannakhet', 'ສະຫວັນນະເຂດ'),
    ('Salavan', 'ສາລະວັນ'),
    ('Sekong', 'ເຊກອງ'),
    ('Champasak', 'ຈຳປາສັກ'),
    ('Attapeu', 'ອັດຕະປື'),
    ('Xaysomboun', 'ໄຊສົມບູນ'),
    ]
         # ປະກາດຕົວເລືອກໄວ້ໃນ class ເລີຍ
    GRADUATE_CHOICES = [
        ('ມໍ7', 'ຈົບມໍ7ແລ້ວ (已毕业)'),
        ('ຍັງບໍ່ຈົບ', 'ຍັງບໍ່ຈົບ (未毕业)'),
    ]
    
    chinese_level1 = [
        ('HSK1', 'HSK1'),
        ('HSK2', 'HSK2'),
        ('HSK3', 'HSK3'),
        ('HSK4', 'HSK4'),
        ('HSK5', 'HSK5'),
        ('HSK6', 'HSK6'),
    ]
    ETHNICITY_CHOICES = [
        ('Lao', 'ລາວ'),
        ('Hmong', 'ມົ້ງ'),
        ('Khmu', 'ກຶມມຸ'),
        ('Phouthai', 'ຜູ້ໄທ'),
        ('Tai', 'ໄຕ'),
        ('Other', 'ອື່ນໆ (Other)'),
    ]

    RELIGION_CHOICES = [
        ('Buddhism', 'ພຸດ'),
        ('Christianity', 'ຄຣິດ'),
        ('Islam', 'ອິດສະລາມ'),
        ('Animism', 'ນັບຖືຜີ / ບໍ່ມີສາດສະໜາ'),
        ('Other', 'ອື່ນໆ (Other)'),
    ]
     # ... (ຟີວອື່ນໆຂອງທ່ານ) ...
    student_code = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        # 1. ກວດສອບກ່ອນວ່າເປັນການເພີ່ມຂໍ້ມູນໃໝ່ແທ້ບໍ່ (ຖ້າຍັງບໍ່ມີ ID ສະແດງວ່າເປັນຂໍ້ມູນໃໝ່)
        is_new = self.pk is None 
        
        # 2. ບັນທຶກຮອບທຳອິດເພື່ອເອົາ ID ທີ່ແທ້ຈິງມາຈາກ SQLite ກ່ອນ
        super(FormResponse, self).save(*args, **kwargs)

        # 3. ຖ້າເປັນຂໍ້ມູນໃໝ່ ແລະ ຊ່ອງ student_code ຍັງຫວ່າງຢູ່
        if is_new and not self.student_code:
            # ສ້າງລະຫັດ VITA ໂດຍເອົາ ID ທີ່ໄດ້ມາຕື່ມເລກ 0 ທາງໜ້າໃຫ້ຄົບ 3 ຫຼັກ (ໃຫ້ຄືກັບຖານຂໍ້ມູນເກົ່າຂອງທ່ານ ເຊັ່ນ: VITA018)
            self.student_code = f"VITA{self.id:03d}"
            
            # 4. ບັນທຶກທັບລົງໄປຖານຂໍ້ມູນອີກຮອບໜຶ່ງ ເພື່ອອັບເດດລະຫັດ
            super(FormResponse, self).save(update_fields=['student_code'])
    # ຄໍລຳ A: Timestamp (ເວລາທີ່ບັນທຶກຟອມ)
    timestamp = models.DateTimeField(
    verbose_name="Timestamp", 
    default=timezone.now
    )
    
    # ຄໍລຳ B: ຊື່ ແລະ ນາມສະກຸນ(ຈິງ)
    full_name = models.CharField(
        max_length=255, 
        verbose_name="ຊື່ ແລະ ນາມສະກຸນລາວ(真实姓名)"
    )

    name_Chinese = models.CharField(
        max_length=255,blank=True,
        verbose_name="ຊື່ແທ້ພາສາຈີນ ຫຼື ອັງກິດ(真实姓名)"
    )
     # 📅 ເພີ່ມຟິວ ວັນເດືອນປີເກີດ (Date of Birth) ໄວ້ຖັດຈາກ Timestamp
    date_of_birth = models.DateField(
        verbose_name="ວັນເດືອນປີເກີດ (出生日期)",
        blank=True,
        null=True
    )
        # 👥 ຟິວຊົນເຜົ່າ (Ethnicity)
    ethnicity = models.CharField(
        max_length=50,
        choices=ETHNICITY_CHOICES,
        default='Lao',
        verbose_name="ຊົນເຜົ່າ (民族)"
    )
    # 💡 ເພີ່ມຟິວນີ້: ກັນໄວ້ກໍລະນີເລືອກ "ອື່ນໆ" ໃນຊົນເຜົ່າ
    ethnicity_other = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="ຊົນເຜົ່າອື່ນໆ (请ກອກຊົນເຜົ່າຂອງທ່ານ)"
    )

    # 🕋 ຟິວສາສະໜາ (Religion)
    religion = models.CharField(
        max_length=50,
        choices=RELIGION_CHOICES,
        default='Buddhism',
        verbose_name="ສາດສະໜາ (宗教)"
    )
    # 💡 ເພີ່ມຟິວນີ້: ກັນໄວ້ກໍລະນີເລືອກ "ອື່ນໆ" ໃນສາດສະໜາ
    religion_other = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="ສາດສະໜາອື່ນໆ (请ກອກສາດສະໜາຂອງທ່ານ)"
    )

    # ຄໍລຳ C: ມາຈາກພາກສ່ວນ/ໂຮງຮຽນໃດ
    organization = models.CharField(
        max_length=255, 
        verbose_name="ມາຈາກໂຮງຮຽນໃດ(来自哪所学校？)"
    )
    # ຄໍລຳ D: ບ້ານ (城市)
    Village = models.CharField(
        max_length=100, 
        verbose_name="ບ້ານ (村莊)",
        blank=True
    )
        
    # ຄໍລຳ D: ເມືອງ (城市)
    district = models.CharField(
        max_length=100, 
        verbose_name="ເມືອງ (城市)"
    )
    
    # ຄໍລຳ E: ແຂວງ (省)
    province1 = models.CharField(
        max_length=60, 
        choices=PROVINCE_CHOICES3, 
        default='ນະຄອນຫຼວງວຽງຈັນ',
        verbose_name="ແຂວງເກີດ (省)"
    )

    
    # ຄໍລຳ F: ຈົບມໍ 7 ຫຼື ບໍ່? (你七年级毕业嘛)
    is_graduated_m7 = models.CharField(
        max_length=20,
        choices=GRADUATE_CHOICES,
        verbose_name="ຫຼັງຈາກເດືອນ9 ສົກ2026 ນີ້ນ້ອງຮຽນຊັ້ນໃດ? (你七年级毕业嘛)"
    )
          
    # ຄໍລຳ G: ຖ້າບໍ່ຈົບ, ປັດຈຸບັນຮຽນຢູ່ຊັ້ນໃດ?
    current_grade = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name="ຖ້າບໍ່ຈົບ, ປັດຈຸບັນຮຽນຢູ່ຊັ້ນໃດ?"
    )  
    # ຄໍລຳ H: ລະດັບພາສາຈີນ (中文)
    chinese_level = models.CharField(
        max_length=60,
        blank=True,
        choices=chinese_level1, 
        verbose_name="ລະດັບພາສາຈີນ (中文)"
    )
    
    # ຄໍລຳ I: ເບີຕິດຕໍ່ (联络手机)
    phone_number = models.CharField(
        max_length=50, 
        verbose_name="ເບີຕິດຕໍ່ (联络手机)"
    )

    facebook = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name="facebook (脸书)"
    )
    
    # 📸 ເພີ່ມຟິວສຳລັບເກັບຮູບພາບ (ຮູບພາບຈະຖືກອັບໂຫລດໄປໄວ້ໃນໂຟນເດີ uploads/ )
    image = models.ImageField(
        upload_to='uploads/', 
        blank=True, 
        null=True, 
        verbose_name="ຮູບພາບແນບມາ"
    )
    subject_set = models.ManyToManyField(
        Subject,
        verbose_name="ວິຊາເລືອກຮຽນທີ່ສູນປາລີ (选修课程)"
        )

    class Meta:
        verbose_name = "ຂໍ້ມູນການລົງທະບຽນນັກຮຽນທືນວິຕ້າ"
        verbose_name_plural = "ຂໍ້ມູນການລົງທະບຽນນັກຮຽນທືນວິຕ້າ"

    def __str__(self):
        return f"{self.full_name} - {self.organization}"
        # 💡 ເພີ່ມໂຄດຊຸດນີ້ເຂົ້າໄປທາງລຸ່ມສຸດຂອງ class FormResponse ໃນ models.py
    # 💡 ວາງໄວ້ທາງລຸ່ມສຸດ ພາຍໃນ class FormResponse
    def save(self, *args, **kwargs):
        # 1. ສັ່ງ Save ປົກກະຕິເພື່ອໃຫ້ໄດ້ຟາຍຮູບມາກ່ອນ
        super().save(*args, **kwargs)

        # 2. 🚀 ກັນໄວ້: ບີບອັດຮູບພາບໃຫ້ເຫຼືອຟາຍນ້ອຍໆອັດຕະໂນມັດ ຖ້າມີການອັບໂຫລດຮູບ
        if self.image:
            from PIL import Image
            import os

            img_path = self.image.path
            if os.path.exists(img_path):
                img = Image.open(img_path)

                # ຫຍໍ້ຂະໜາດໃຫ້ພໍດີຕິດໃບ CV (ກວ້າງ 240px, ສູງ 320px ພໍດີງາມ)
                if img.width > 240 or img.height > 320:
                    output_size = (240, 320)
                    img.thumbnail(output_size)
                    # Save ທັບຟາຍເກົ່າ ພ້ອມຫຼຸດຄຸນນະພາບ (Quality) ໃຫ້ຟາຍເບົາເຄື່ອງ 🚀
                    img.save(img_path, quality=75, optimize=True)