from django.db import models
from django.contrib.admin.decorators import display
from django.db.models import Model
from django.db.models.fields.files import ImageField
from django.template.loader import get_template
from django import forms 
    
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
         # ປະກາດຕົວເລືອກໄວ້ໃນ class ເລີຍ
    GRADUATE_CHOICES = [
        ('ມໍ7', 'ຈົບແລ້ວ (已毕业)'),
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
   
    # ຄໍລຳ A: Timestamp (ເວລາທີ່ບັນທຶກຟອມ)
    timestamp = models.DateTimeField(
        verbose_name="Timestamp", 
        auto_now_add=True
    )
    
    # ຄໍລຳ B: ຊື່ ແລະ ນາມສະກຸນ(ຈິງ)
    full_name = models.CharField(
        max_length=255, 
        verbose_name="ຊື່ ແລະ ນາມສະກຸນ(真实姓名)"
    )

    name_Chinese = models.CharField(
        max_length=255,blank=True,unique=True,
        verbose_name="ຊື່ ແລະ ນາມສະກຸນພາສາຈີນ(真实姓名)"
    )
    
    # ຄໍລຳ C: ມາຈາກພາກສ່ວນ/ໂຮງຮຽນໃດ
    organization = models.CharField(
        max_length=255, 
        verbose_name="ມາຈາກໂຮງຮຽນໃດ(来自哪所学校？)"
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
        verbose_name="ແຂວງ (省)"
    )

    
    # ຄໍລຳ F: ຈົບມໍ 7 ຫຼື ບໍ່? (你七年级毕业嘛)
    is_graduated_m7 = models.CharField(
        max_length=20,
        choices=GRADUATE_CHOICES,
        verbose_name="ຈົບມໍ 7 ຫຼື ບໍ່? (你七年级毕业嘛)"
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
        verbose_name="ວິຊາເລືອກຮຽນ (选修课程)"
        )

    class Meta:
        verbose_name = "ຂໍ້ມູນການລົງທະບຽນ"
        verbose_name_plural = "ຂໍ້ມູນການລົງທະບຽນສອບເສັງພາສາຈີນ"

    def __str__(self):
        return f"{self.full_name} - {self.organization}"
