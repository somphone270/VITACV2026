from django import forms
from django.forms.widgets import TextInput, Select, CheckboxSelectMultiple, Textarea, FileInput
from myapp.models import Subject, Subscription
from .models import FormResponse
class SubjectMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class SubscriptionModelForm(forms.ModelForm):
    # 1. ຟິວວັນເກີດ (Custom Widget & Validation)
    birthday = forms.DateField(
        label='ວັນເດືອນປີເກີດ',
        required=True,
        input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'YYYY-MM-DD',
            'onfocus': "this.type='date'",
            'onblur': "if(this.value==''){this.type='text'}"
        })
    )

    # 2. ຟິວເລືອກສາຂາວິຊາ (Custom Queryset & Checkbox)
    subject_set = SubjectMultipleChoiceField(
        queryset=Subject.objects.order_by('-is_premium'),
        required=True,
        label='ສາຂາຮຽນທີ່ສົນໃຈ :',
        widget=CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )

    # 3. ຟິວປຸ່ມຕິກຢືນຢັນ (BooleanField ທີ່ບໍ່ມີໃນ Model ແຕ່ໃຊ້ກວດສອບໃນຟອມ)
    accepted = forms.BooleanField(
        required=True,
        label="ຂ້ອຍຢືນຢັ້ງວ່າຂໍ້ມູນທັງໝົດແມ່ນຖືກຕ້ອງ",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Subscription
        # ດຶງທຸກຟິວມາສະແດງ ແລະ ລຽງລຳດັບໃຫ້ເປັນໝວດໝູ່ຢ່າງສວຍງາມ
        fields = [
            # ໝວດຂໍ້ມູນສ່ວນຕົວ
            'StudentID', 'gender', 'gender_eng', 'name', 'Username_lao', 
            'name_eng', 'Username_eng', 'age', 'birthday', 'photo', 
            'Profile', 'Nationality', 'Religion','Buddhism',
            
            # ໝວດຂໍ້ມູນການຕິດຕໍ່ / ທີ່ຢູ່ຕາມທະບຽນບ້ານ
            'email', 'tel','Mobile_Parents', 'province', 'districts', 'village',
            
            # ໝວດທີ່ຢູ່ປັດຈຸບັນ
            'Current_province', 'Current_districts', 'Current_village', 
            
            # ໝວດການສຶກສາ ແລະ ການເຮັດວຽກ
            'from_school', 'academic_year', 'semester', 'employee', 'subject',
            'province_school', 'districts_school', 'village_school',
            
            # ໝວດທັກສະ ແລະ ສະຖານະລະບົບ
            'Skill', 'Other_Skill', 'Language', 'Language1', 'Language2',
            'status', 'subject_set', 'accepted'
        ]
        
        # ຄຳອະທິບາຍພາສາລາວສຳລັບທຸກໆ Field
        labels = {
            # Personal Info
            'StudentID': 'ລະຫັດນັກຮຽນ/ນັກສຶກສາ',
            'gender': 'ນາມມະຍຸດນຳໜ້າ (ພາສາລາວ)',
            'gender_eng': 'ນາມມະຍຸດນຳໜ້າ (ພາສາອັງກິດ)',
            'name': 'ຊື່ແທ້ (ພາສາລາວ)',
            'Username_lao': 'ນາມສະກຸນ (ພາສາລາວ)',
            'name_eng': 'ຊື່ແທ້ເປັນ (ພາສາອັງກິດ)',
            'Username_eng': 'ນາມສະກຸນເປັນ (ພາສາອັງກິດ)',
            'age': 'ອາຍຸ',
            'birthday': 'ວັນເດືອນປີເກີດ',
            'photo': 'ຮູບຖ່າຍ/ຮູບໂປຣຟາຍ',
            'Profile': 'ປະຫວັດສ່ວນຕົວຫຍໍ້',
            'Nationality': 'ສັນຊາດ',
            'Religion': 'ຊົນເຜົ່າ',
            'Buddhism': 'ສາສະໜາ',
            
            # Contact Info
            'email': 'ອີເມວ',
            'tel': 'ເບີໂທຕິດຕໍ່',
            'province': 'ແຂວງ (ແຂວງເກີດ)',
            'districts': 'ເມືອງ (ເມືອງເກີດ)',
            'village': 'ບ້ານ (ບ້ານເກີດ)',
            'Current_province': 'ແຂວງ (ທີ່ຢູ່ປັດຈຸບັນ)',
            'Current_districts': 'ເມືອງ (ທີ່ຢູ່ປັດຈຸບັນ)',
            'Current_village': 'ບ້ານ (ທີ່ຢູ່ປັດຈຸບັນ)',
            'Mobile_Parents': 'ເບີຕິດຕໍ່ຜູ້ປົກຄອງ (ເບີໂທທີ່ສາມາດຕິດຕໍ່ໄດ້)',
            
            # Education & Work
            'from_school': 'ມາຈາກໂຮງຮຽນ/ສະຖາບັນ',
            'academic_year': 'ປີການສຶກສາ/ສົກຮຽນ',
            'semester': 'ພາກຮຽນ',
            'employee': 'ສະຖານທີ່ເຮັດວຽກ/ອາຊີບ',
            'subject': 'ສາຂາວິຊາຮຽນ',
            'province_school': 'ແຂວງ ຂອງໂຮງຮຽນ',
            'districts_school': 'ເມືອງ ຂອງໂຮງຮຽນ',
            'village_school': 'ບ້ານ ຂອງໂຮງຮຽນ',
            
            # Skills & System
            'Skill': 'ທັກສະຄວາມຮູ້',
            'Other_Skill': 'ທັກສະອື່ນໆ',
            'Language': 'ພາສາຕ່າງປະເທດ 1',
            'Language1': 'ພາສາຕ່າງປະទេດ 2',
            'Language2': 'ພາສາຕ່າງປະເທດ 3',
            'status': 'ສະຖານະການອະນຸມັດ',
            'subject_set': 'ສາຂາຮຽນທີ່ສົນໃຈ',
            'accepted': 'ຢືນຢັ້ງຄວາມຖືກຕ້ອງ'
        }
        
        # ກຳນົດ HTML Widgets ເພີ່ມເຕີມເພື່ອຄວາມເໝາະສົມກັບຟິວແຕ່ລະປະເພດ
        widgets = {
            'gender': Select(attrs={'class': 'form-control'}),
            'gender_eng': Select(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control'}),
            'photo': FileInput(attrs={'class': 'form-control-file'}),
            'Profile': Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'ອະທິບາຍປະຫວັດຫຍໍ້ຂອງທ່ານ...'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ວົນລູບອັດຕະໂນມັດເພື່ອໃສ່ class 'form-control' ໃຫ້ຟິວທົ່ວໄປ (ຊ່ວຍໃຫ້ Bootstrap ສະແດງຜົນງາມ)
        # ໂດຍເວັ້ນຟິວປະເພດ Checkbox, File, Textarea ແລະ Select ທີ່ເຮົາ Custom ໄວ້ແລ້ວ
        excluded_fields = ['birthday', 'subject_set', 'accepted', 'gender', 'gender_eng', 'status', 'photo', 'Profile']
        for field_name, field in self.fields.items():
            if field_name not in excluded_fields:
                field.widget.attrs.update({'class': 'form-control'})


from .models import FormResponse

class RegistrationForm(forms.ModelForm):
    # 💡 ປະກາດຟິວ date_of_birth ແຍກອອກມາທາງເທິງເພື່ອຮອງຮັບຮູບແບບ ວັນ/ເດືອນ/ປີ (DD/MM/YYYY)
    date_of_birth = forms.DateField(
        input_formats=['%d/%m/%Y', '%Y-%m-%d'],  # ຮອງຮັບທັງການພິມແບບລາວ ແລະ ຮູບແບບຖານຂໍ້ມູນ
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ວັນ/ເດືອນ/ປີ (ຕົວຢ່າງ: 25/12/2005)',
            'inputmode': 'numeric',              # 📱 ບັງຄັບໃຫ້ໂທລະສັບເປີດແປ້ນພິມຕົວເລກທັນທີ
            'pattern': '[0-9]{2}/[0-9]{2}/[0-9]{4}', # ກຳນົດໃຫ້ພິມເປັນ ວັນ/ເດືອນ/ປີ ເທົ່ານັ້ນ
        }),
        label="ວັນເດືອນປີເກີດ (出生日期)",
        required=False
    )

    class Meta:
        model = FormResponse
        # 1. ເພີ່ມ 'ethnicity' ແລະ 'religion' ເຂົ້າໄປໃນລາຍການ fields (ໄວ້ຖັດຈາກ date_of_birth)
        fields = [
            'full_name', 'name_Chinese', 'date_of_birth', 
            'ethnicity', 'ethnicity_other',  # 💡 ເພີ່ມ ethnicity_other
            'religion', 'religion_other',    # 💡 ເພີ່ມ religion_other
            'organization', 'Village', 'district', 'province1', 
            'is_graduated_m7', 'current_grade', 'chinese_level', 
            'subject_set', 'phone_number', 'facebook', 'image'
        ]
        
        # 2. ຕົບແຕ່ງ Form Style (ເພີ່ມ widget Dropdown ສຳລັບຊົນເຜົ່າ ແລະ ສາດສະໜາ)
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ທ້າວ/ນາງ ...'}),
            'name_Chinese': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '先生/女士……'}),
            
            # 💡 ກຳນົດໃຫ້ເປັນ Select (Dropdown ລາຍການເລືອກ) ພ້ອມກັບ Bootstrap class
            # (widgets ໂຕອື່ນໆ ປ່ອຍໄວ້ຄືເກົ່າ...)
            'ethnicity': forms.Select(attrs={'class': 'form-control'}),
            'religion': forms.Select(attrs={'class': 'form-control'}),
            
            # 💡 ຕົບແຕ່ງຊ່ອງພິມ "ອື່ນໆ" ໃຫ້ສວຍງາມ
            'ethnicity_other': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ພິມຊົນເຜົ່າຂອງທ່ານ...'}),
            'religion_other': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ພິມສາດສະໜາຂອງທ່ານ...'}),
            
            'organization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ໂຮງຮຽນ ຫຼື ມະຫາວິທະຍາໄລ...'}),
            'Village': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ບ້ານ...'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ເມືອງ...'}),
            'province1': forms.Select(attrs={'class': 'form-control'}),
            'is_graduated_m7': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'current_grade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ມໍ4, ມໍ5, ມໍ6, ...'}),
            'chinese_level': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'subject_set': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '020...'}),
            'facebook': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ຊື່ Facebook...'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ສັ່ງລຶບຄ່າຫວ່າງ (---------) ອອກຈາກປຸ່ມ Radio ທັງສອງຟິວ
        if 'is_graduated_m7' in self.fields:
            self.fields['is_graduated_m7'].empty_label = None
        if 'chinese_level' in self.fields:
            self.fields['chinese_level'].empty_label = None
            
        # 💡 ກັນໄວ້: ສັ່ງລຶບຄ່າຫວ່າງ (---------) ອອກຈາກ Dropdown ຂອງຊົນເຜົ່າ ແລະ ສາດສະໜາ ນຳເຊັ່ນກັນ
        if 'ethnicity' in self.fields:
            self.fields['ethnicity'].empty_label = None
        if 'religion' in self.fields:
            self.fields['religion'].empty_label = None
        
        # ດຶງຂໍ້ມູນ Subject ທັງໝົດມາສະແດງ
        if 'subject_set' in self.fields:
            self.fields['subject_set'].queryset = Subject.objects.all()