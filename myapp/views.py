from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from myapp.forms import SubscriptionModelForm
from myapp.models import Subject
from django.http import HttpResponse
from myapp.models import Subscription
from .forms import RegistrationForm
from .models import FormResponse
import xlwt
from django.shortcuts import render
from .models import FormResponse, Subject
from django.db.models import Q

from .models import FormResponse, Subject

from django.shortcuts import render
from .models import FormResponse, Subject
from django.db.models import Q

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.views import LoginView

# 💡 ສ້າງ Class ຫຸ້ມລະບົບ Login ຂອງ Admin ເພື່ອເພີ່ມການກວດສອບ
class CustomAdminLoginView(LoginView):
    form_class = AdminAuthenticationForm
    template_name = 'admin/login.html' # ບັງຄັບໃຫ້ໃຊ້ Template ຂອງ Admin

    def form_invalid(self, form):
        # 🔥 ດັກຈັບເວລາລະຫັດຜ່ານຜິດ ຫຼື ບໍ່ມີສິດເປັນ Admin ແລ້ວສົ່ງຂໍ້ຄວາມເຕືອນ
        messages.error(self.request, 'ຊື່ຜູ້ໃຊ້ ຫຼື ລະຫັດຜ່ານ Admin ບໍ່ຖືກຕ້ອງ! (管理员用户名หรือ密码错误)')
        return super().form_invalid(form)


def home(request):
    # 1. ຮັບຄ່າຄຳຄົ້ນຫາ, ສົກຮຽນ ແລະ Action (ເພີ່ມ action ເຂົ້າມາ)
    search_query = request.GET.get('search', '')
    school_year_query = request.GET.get('school_year', '')
    action = request.GET.get('action', '')  # 🔥 ເພີ່ມແຖວນີ້ເພື່ອເຊັກປຸ່ມກົດ

    # 2. ເລີ່ມຕົ້ນດຶງຂໍ້ມູນທັງໝົດອອກມາລຽງຕາມ ID
    users_queryset = FormResponse.objects.all().order_by('id')
    all_subjects = Subject.objects.all().order_by('id')

    # 3. ລະບົບກັ່ນຕອງຂໍ້ມູນ (Filter) ຕາມຊ່ອງຄົ້ນຫາ
    if search_query:
        users_queryset = users_queryset.filter(
            Q(full_name__icontains=search_query) |
            Q(organization__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(district__icontains=search_query) |
            Q(province1__icontains=search_query)
        )

    # 4. ກັ່ນຕອງສົກຮຽນ ໂດຍອ້າງອີງຈາກ "ປີ" ຂອງຟີວ timestamp
    if school_year_query:
        if school_year_query == '2027':
            users_queryset = users_queryset.filter(timestamp__year__in=[2027])
        elif school_year_query == '2026':
            users_queryset = users_queryset.filter(timestamp__year__in=[2026])
        elif school_year_query == '2025':
            users_queryset = users_queryset.filter(timestamp__year__in=[2025])
        elif school_year_query == '2024':
            users_queryset = users_queryset.filter(timestamp__year__in=[2024])

    # 5. ນັບຈຳນວນນັກສຶກສາທີ່ຖືກກັ່ນຕອງແລ້ວ
    total_students_count = users_queryset.count()

    # 6. ສ້າງ Context ຂໍ້ມູນ
    context = {
        'users': users_queryset,
        'subjects': all_subjects,
        'total_count': total_students_count,
        'search_query': search_query,
        'school_year_query': school_year_query,
    }

    # 🔥 7. ຈຸດແຍກໜ້າ: ຖ້າມີການສົ່ງ ?action=print ມາໃຫ້ເປີດໜ້າ CV ທັງໝົດ, ຖ້າບໍ່ມີໃຫ້ເປີດໜ້າໂຮມປົກກະຕິ
    if action == 'print':
        return render(request, 'view_all_cv.html', context)
        
    return render(request, 'home.html', context)




def about(request):
    return render(request, 'about.html')

def Borntobeaschool(request):
    return render(request, 'Borntobeaschool.html')

def Context(request):
    return render(request, 'Context.html')

def subscription(request):
    if request.method == 'POST':      
        form = SubscriptionModelForm(request.POST)
        if form.is_valid():          
            form.save()    
            return HttpResponseRedirect(reverse('subscription_done'))    
        else:
            print("Form Errors:", form.errors)  
    else: 
        form = SubscriptionModelForm()
    return render(request, 'subscription_form.html', {'form': form})

def subscription_done(request):
    return render(request, 'subscription_done.html')


def preview_all(request):
    return render(request, 'preview_all.html')


def subject_list(request):
     subjects = Subject.objects.all()
     return render(request, 'subject.html', {'subjects': subjects})  
 

def subject_detail(request, subject_id):
    one_subject = Subject.objects.get(id=subject_id)
    context = {'subject1': one_subject}
    return render(request, 'myapp/subject_detail.html', context)


def cv_detail(request, sub_id):
    one_sub =FormResponse.objects.get(id=sub_id)
    context = {'user': one_sub}
    return render(request, 'myapp/Create_CV.html', context)


def studyimages(request):
    return render(request, 'studyimages.html')

# ✅ Export to Excel
def export_subscriptions_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="subscriptions.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Subscriptions')

    row_num = 0
    columns = [
        'ID', 'ຊື່', 'ຊື່ອັງກິດ', 'ເພດ', 'ອາຍຸ', 'ວັນເກີດ',
        'ອີເມວ', 'ໂທລະສັບ', 'ແຂວງ', 'ເມືອງ', 'ບ້ານ',
        'ຈາກໂຮງຮຽນ', 'ປີການສຶກສາ', 'ພາກຮຽນ', 'ສະຖານະ', 'ວັນທີ່ລົງທະບຽນ'
    ]

    for col_num, column_title in enumerate(columns):
        ws.write(row_num, col_num, column_title)

    rows = Subscription.objects.all().values_list(
        'id', 'name', 'name_eng', 'gender', 'age', 'birthday',
        'email', 'tel', 'province', 'districts', 'village',
        'from_school', 'academic_year', 'semester', 'status', 'registered_at'
    )

    for row in rows:
        row_num += 1
        for col_num, cell_value in enumerate(row):
            ws.write(row_num, col_num, str(cell_value))
    wb.save(response)
    return response


# views.py
from django.shortcuts import render, redirect
from django.contrib import messages  # 💡 1. ຕ້ອງອິມພອດ messages ມາຊ່ວຍແຈ້ງເຕືອນ
from .forms import RegistrationForm

from django.shortcuts import render, redirect
from .forms import RegistrationForm  # ປ່ຽນເປັນຊື່ຟອມຂອງທ່ານ
from django.shortcuts import render, redirect
from .forms import RegistrationForm  # ປ່ຽນເປັນຊື່ຟອມຂອງທ່ານ

import base64
import uuid  # ເພີ່ມເຂົ້າມາເພື່ອຕັ້ງຊື່ຮູບໃຫ້ບໍ່ຊ້ຳກັນ
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from .forms import RegistrationForm  # ປ່ຽນເປັນຊື່ຟອມຂອງທ່ານ

import base64
import uuid
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from .forms import RegistrationForm  # ປ່ຽນເປັນຊື່ຟອມຂອງທ່ານ

import base64
import uuid
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from .forms import RegistrationForm  # ປ່ຽນເປັນຊື່ຟອມຂອງທ່ານ
import base64
import uuid
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile

import base64
import uuid
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile

import base64
import uuid
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect

import base64
import uuid
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect

def register_view(request):
    custom_error = None
    form_has_errors = "false"
    
    if request.method == 'POST':
        post_data = request.POST.copy()
        form = RegistrationForm(post_data, request.FILES)
        image_base64 = request.POST.get('image_base64')
        img_bytes = None
        ext = 'jpg'
        
        if image_base64 and ';base64,' in image_base64:
            try:
                format, imgstr = image_base64.split(';base64,')
                ext = format.split('/')[-1]
                img_bytes = base64.b64decode(imgstr)
            except Exception as e:
                print(f"Error decoding base64: {e}")
                
        if form.is_valid() and img_bytes:
            obj = form.save(commit=False)
            file_name = f"profile_{uuid.uuid4().hex[:8]}.{ext}"
            obj.image.save(file_name, ContentFile(img_bytes), save=False)
            
            # 1. 💾 ບັນທຶກຂໍ້ມູນຮອບທີ 1 ເພື່ອເອົາເລກ ID ທີ່ແທ້ຈິງມາຈາກ SQLite ກ່ອນ
            obj.save()
            form.save_m2m()
            
            # 2. ⚡ ບັງຄັບໃຫ້ Python ເປັນຄົນສ້າງລະຫັດ VITA ຝັງລົງໄປເອງເລີຍ (ຕັດບັນຫາ Trigger ເຮັດວຽກບໍ່ທັນ)
            # ມັນຈະເອົາ ID ມາເຮັດເປັນເລກ 3 ຫຼັກ ເຊັ່ນ ID = 59 -> VITA059
            obj.student_code = f"VITA{obj.id:03d}"
            
            # 3. 💾 ບັນທຶກທັບລົງໄປຖານຂໍ້ມູນອີກຮອບໜຶ່ງ ເພື່ອອັບເດດລະຫັດໃຫ້ຊົວຣ໌
            obj.save(update_fields=['student_code'])
            
            # 4. 🚀 ສົ່ງ ID ໄປຫາໜ້າ Success ຜ່ານ URL Parameter 
            return redirect(f'/success/?student_id={obj.id}') 
        else:
            form_has_errors = "true"
            if not img_bytes:
                custom_error = "❌ ກະລຸນາເລືອກ ແລະ ຕັດຮູບພາບໃບໜ້າ 3x4 ຂອງທ່ານ."
    else:
        form = RegistrationForm()
        
    return render(request, 'register.html', {
        'form': form,
        'custom_error': custom_error,
        'form_has_errors': form_has_errors
    })


# 🎯 ຟັງຊັນໜ້າ Success: ດຶງ ID ຈາກ URL ມາ Query ຫາຄ່າ student_code ຕົວຈິງ
def success_view(request):
    db_student_id = request.GET.get('student_id', None)
    actual_student_code = None
    
    if db_student_id:
        try:
            # 🔄 ດຶງ Model ມາຈາກ Form ໂດຍກົງ ເພື່ອປ້ອງກັນບັນຫາຊື່ Model ຜິດພາດ
            ModelClass = RegistrationForm.Meta.model
            
            # 🔍 Query ໄປຄົ້ນຫາຂໍ້ມູນແຖວນັ້ນໃນ Database ໃໝ່ສົດໆ ໂດຍໃຊ້ ID
            student_obj = ModelClass.objects.get(id=db_student_id)
            
            # ດຶງເອົາຄ່າ student_code ທີ່ຖືກບັນທຶກໄວ້ໃນ SQLite ອອກມາ (ເຊັ່ນ: VITA059)
            actual_student_code = student_obj.student_code
        except Exception as e:
            print(f"❌ Error querying student_code: {e}")
        
    # ⚠️ ສຳຄັນທີ່ສຸດ: ສົ່ງຄ່າຕົວແປ 'student_code' (ຊື່ຕ້ອງກົງກັບໃນ HTML ເປະໆ)
    return render(request, 'success.html', {'student_code': actual_student_code})



def qr_scanner_view(request):
    """ໜ້າເວັບສໍາລັບເປີດກ້ອງສະແກນ QR"""
    return render(request, 'qr_scanner.html')
from django.http import JsonResponse

import re
from django.http import JsonResponse
from django.shortcuts import render
from .models import FormResponse

import re
from django.http import JsonResponse
from django.shortcuts import render
from .models import FormResponse # 💡 ກວດສອບຊື່ App ຂອງທ່ານຄືນໃຫ້ຖືກຕ້ອງ

import re
from django.http import JsonResponse
from django.shortcuts import render
from .models import FormResponse 

import re
from django.http import JsonResponse
from django.shortcuts import render
from .models import FormResponse  # 💡 ກວດສອບຊື່ App ຂອງທ່ານຄືນໃຫ້ຖືກຕ້ອງ

def check_registration_api(request, registration_id=None):
    """API ສໍາລັບກວດສອບຂໍ້ມູນ ທີ່ຮອງຮັບ VITA002, VITA-002 ແລະ ຕົວເລກລ້ວນ 002 ຫຼື 2"""
    if registration_id is not None:
        try:
            # 1. ຕັດຫວ່າງ ແລະ ແປງເປັນຕົວພິມໃຫຍ່
            clean_id = str(registration_id).strip().upper()

            # 2. 💡 ປັບ Regex ໃໝ່: ^([A-Z-]*)([0-9]+)$
            # ບັງຄັບໃຫ້ໂຄງສ້າງມີແຕ່ ຕົວອັກສອນ/ຂີດຕໍ່ ຢູ່ທາງໜ້າ ແລະ ຕາມດ້ວຍ ຕົວເລກ ຢູ່ທາງຫຼັງເທົ່ານັ້ນ
            # ຖ້າມີຕົວອັກສອນປົນມາທາງຫຼັງຕົວເລກ (ເຊັ່ນ VITA002tyu) ຈະຖືກບລັອກທັນທີ
            if not re.match(r'^([A-Z-]*)([0-9]+)$', clean_id):
                return JsonResponse({
                    'success': False,
                    'message': '⚠️ ຮູບແບບລະຫັດບໍ່ຖືກຕ້ອງ! ຫ້າມມີຕົວອັກສອນອື່ນປົນປອມ (编号格式错误)'
                })

            # 3. ດຶງເອົາສະເພາະຕົວເລກອອກມາ (ເຊັ່ນ: "VITA002" -> "002", "011" -> "011", "2" -> "2")
            numeric_id = ''.join(re.findall(r'\d+', clean_id))
            if not numeric_id:
                return JsonResponse({
                    'success': False,
                    'message': '⚠️ ບໍ່ພົບຕົວເລກໃນລະຫັດ! (编号格式错误)'
                })

            # 4. ຈັດ Format ເລກໃຫ້ເປັນ 3 ຫຼັກ (ເຊັ່ນ: ເລກ 2 ຈະກາຍເປັນ "002") ເພື່ອໃຫ້ຕົງກັບ STUDENT CODE
            formatted_number = f"{int(numeric_id):03d}" 

            # 5. คົ້ນຫາແບບຕົງເປະ 100% (__exact) ກັບ STUDENT CODE ໃນຖານຂໍ້ມູນ
            # ປ່ຽນ student_code ໃຫ້ກົງກັບ Field ແທ້ໃນ Model ຂອງທ່ານ
            student = FormResponse.objects.get(student_code__exact=f"VITA{formatted_number}")

            # 6. ດຶງຄ່າຊັ້ນຮຽນປັດຈຸບັນມາຈາກ Database ໂດຍກົງ
            grade_display = getattr(student, 'current_grade', '-')

            data = {
                'success': True,
                'name': student.full_name,
                'name_eng': student.name_Chinese,
                'birthday': student.date_of_birth,
                'From_school': student.organization,
                'status_text': "ລົງທະບຽນແລ້ວ / 已註冊",  
                'grade_text': grade_display if grade_display else '-',
                'image_url': student.image.url if hasattr(student, 'image') and student.image else None
            }

        except FormResponse.DoesNotExist:
            data = {
                'success': False,
                'message': f'❌ ບໍ່ພົບຂໍ້ມູນນັກຮຽນລະຫັດ: "VITA{formatted_number}" ໃນລະບົບ!'
            }
        except (ValueError, OverflowError):
            data = {
                'success': False,
                'message': f'❌ ລະບົບປະມວນຜົນລະຫັດ: "{registration_id}" ຜິດພາດ!'
            }
            
        return JsonResponse(data)

    return render(request, 'qr_scanner.html')
