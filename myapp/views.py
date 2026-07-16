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


def home(request):
    # ດຶງຂໍ້ມູນຜູ້ໃຊ້ ແລະ ວິຊາທັງໝົດ ອອກມາລຽງຕາມ ID
    all_users = FormResponse.objects.all().order_by('id')
    all_subjects = Subject.objects.all().order_by('id')
    
    # ສົ່ງຂໍ້ມູນໄປທີ່ Template ໜ້າ home.html
    context = {
        'users': all_users,
        'subjects': all_subjects,  # ປ່ຽນເປັນ 'subjects' ເພື່ອໃຫ້ເປັນພຫູພົດ ເຂົ້າໃຈງ່າຍ
    }
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
    context = {'sub1': one_sub}
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



def register_view(request):
    if request.method == 'POST':
        # ⚠️ ສໍາຄັນຫຼາຍ: ຕ້ອງມີ request.FILES ນຳ ເພື່ອຮັບໄຟລ໌ຮູບພາບ
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save() # ບັນທຶກຂໍ້ມູນ ແລະ ຮູບພາບລົງ Database ທັນທີ
            return redirect('success_page') # ເມື່ອສຳເລັດໃຫ້ຂ້າມໄປໜ້າອື່ນ (ຫຼື ໜ້າເດີມ)
    else:
        form = RegistrationForm()
        
    return render(request, 'register.html', {'form': form})

def success_view(request):
    return render(request, 'success.html')



def qr_scanner_view(request):
    """ໜ້າເວັບສໍາລັບເປີດກ້ອງສະແກນ QR"""
    return render(request, 'qr_scanner.html')

def check_registration_api(request, registration_id):
    """API ສໍາລັບກວດສອບຂໍ້ມູນຫຼັງຈາກສະແກນ QR Code ເຫັນ ID"""
    try:
        # ຄົ້ນຫາຂໍ້ມູນຜູ້ລົງທະບຽນຈາກ ID
        student = FormResponse.objects.get(id=registration_id)
        
        # ສົ່ງຂໍ້ມູນກັບໄປສະແດງຜົນຢູ່ໜ້າເວັບ
        data = {
            'success': True,
            'name': f"{student.first_name} {student.last_name}", # ປ່ຽນຟີວໃຫ້ກົງກັບ Model ຂອງທ່ານ
            'status': student.is_graduated_m7,
            'image_url': student.image.url if student.image else None
        }
    except FormResponse.DoesNotExist:
        data = {
            'success': False,
            'message': '❌ ບໍ່ພົບຂໍ້ມູນການລົງທະບຽນນີ້ໃນລະບົບ!'
        }
        
    return JsonResponse(data)
