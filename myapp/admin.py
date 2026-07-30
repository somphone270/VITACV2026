# admin.site.register(Subject, SubjectAdmin)
from import_export import resources
from import_export.fields import Field
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from myapp.models import Subscription, Subject
from django.contrib import admin
from .models import MyModel
from .models import FormResponse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.safestring import mark_safe # <--- ເພີ່ມການ Import ແຖວນີ້
# Resource

class SubscriptionResource(resources.ModelResource):
    subject_names = Field(column_name='subject_names')

    def dehydrate_subject_names(self, obj):
        return ", ".join([s.name for s in obj.subject_set.all()])

    class Meta:
        model = Subscription
        fields = (
            'id', 'name', 'gender', 'name_eng', 'age','profile','Skills','birthday', 'email', 'province',
            'province_school','districts_school','village_school','Mo','Language','Language1','Language2','Nationality',
            'districts', 'village', 'tel', 'from_school', 'academic_year','Religion','Other_Skill',
            'employee', 'semester', 'status', 'registered_at', 'subject_names'
        )

# Subscription Admin
class SubscriptionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = SubscriptionResource
    list_display = [
        'StudentID','gender', 'name','photo', 'name_eng','age', 'birthday', 'email', 'province','subject',
        'districts', 'Current_village','Current_village','Current_districts','province', 'tel', 'from_school', 'academic_year',
        'employee', 'semester', 'status', 'registered_at', 'get_subject_names'
    ]
    search_fields = ['name', 'email']
    list_filter = ['status']

    def get_subject_names(self, obj):
        return ", ".join([s.name for s in obj.subject_set.all()])
    get_subject_names.short_description = 'ສາຂາຮຽນ'

# Subject Admin
class SubjectAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['name', 'Name_eng','is_premium', 'price', 'photo', 'description', 'promotion_end_at']
    search_fields = ['name']

# Register
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(MyModel, fields=('my_image_thumbnail',), readonly_fields=('my_image_thumbnail',))
class FormResponseResource(resources.ModelResource):
    class Meta:
        model = FormResponse
        # 🔥 ກໍານົດໃຫ້ໃຊ້ 'id' ເປັນຕົວເຊັກ (ຖ້າ ID ຊ້ຳ ໃຫ້ອັບເດດຂໍ້ມູນເກົ່າ, ຖ້າບໍ່ຊ້ຳ ໃຫ້ເພີ່ມໃໝ່)
        import_id_fields = ['id'] 
        
        # ບັງຄັບໃຫ້ອັບເດດຂໍ້ມູນທີ່ມີຢູ່ແລ້ວ ຖ້າມີການ Import ຂໍ້ມູນທີ່ ID ຕົງກັນ
        skip_unchanged = True
        report_skipped = True
        
        # ກໍານົດຟີວທີ່ຈະໃຫ້ມີການ Import/Export (ເອົາສະເພາະຟີວທີ່ມີແທ້ໃນຖານຂໍ້ມູນ)
        fields = (
            'id', 'full_name', 'name_Chinese','date_of_birth','organization', 'district', 
            'province1', 'is_graduated_m7', 'current_grade', 'chinese_level', 
            'phone_number', 'facebook', 'image', 'timestamp'
        )
 # 💡 ເພີ່ມຟັງຊັນນີ້ເຂົ້າໄປໃນ Resource ເພື່ອລ້າງ Cache ຂອງ ID ກ່ອນ Import
    def before_import_rows(self, rows, **kwargs):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'myapp_formresponse';")
        super().before_import_rows(rows, **kwargs)   
# ==========================================================================
# 2. ຕົວຈັດການໜ້າ Django Admin
# ==========================================================================

# 💡 ວາງໄວ້ທາງເທິງ class FormResponseAdmin ເດີ້ຄຣັບ ✅
class SchoolYearFilter(admin.SimpleListFilter):
    title = 'ເລືອກປີຮຽນ'  # ຫົວຂໍ້ແຖບກັ່ນຕອງດ້ານຂວາມື
    parameter_name = 'school_year'

    def lookups(self, request, model_admin):
        # 💡 ກຳນົດເປັນຕົວເລກປີໃດປີນັ້ນກົງໆເລີຍ 🚀
        return [
            ('2025', 'ປີ 2025'),
            ('2026', 'ປີ 2026'),
            ('2027', 'ປີ 2027'),
            ('2028', 'ປີ 2028'),
        ]

    def queryset(self, request, queryset):
        # 💡 🚀 ໃຊ້ __year ເພື່ອດັກຈັບ ແລະ ທຽບຄ່າປີໃດປີນັ້ນໂດຍກົງ (ງ່າຍ ແລະ ປອດໄພທີ່ສຸດ) ✅
        if self.value():
            return queryset.filter(timestamp__year=self.value())
        return queryset


@admin.register(FormResponse)
class FormResponseAdmin(ImportExportModelAdmin):
    # 🔥 ດຶງ Resource ທີ່ເຮົາກຳນົດໄວ້ຂ້າງເທິງມາໃຊ້ງານ
    resource_class = FormResponseResource 
    
    # ກໍານົດຄໍລຳທີ່ຈະໃຫ້ສະແດງຢູ່ໜ້າຕາຕະລາງລວມ (ໂຄດເດີມຂອງທ່ານ)
    list_display = (
        'row_number',       # ສະແດງລຳດັບ 1, 2, 3...
        'student_code',
        'show_image',       # ສະແດງຮູບພາບຕົວຢ່າງ
        'full_name',        # ຊື່ ແລະ ນາມສະກຸນ
        'name_Chinese',
        'date_of_birth',
        'ethnicity',
        'ethnicity_other',
        'religion',
        'religion_other',
        'organization',     # ມາຈາກພາກສ່ວນ/ໂຮງຮຽນ
        'district',         # ເມືອງ
        'province1',        # ແຂວງ
        'is_graduated_m7',
        'current_grade',
        'display_subjects',  # ສະແດງວິຊາທີ່ເລືອກ
        'chinese_level',    # ລະດັບພາສາຈີນ
        'phone_number',     # ເບີຕິດຕໍ່
        'facebook',
        'timestamp'         # ເວລາບັນທຶກ
    )

    search_fields = ('full_name', 'organization', 'phone_number', 'district', 'province1')

    # 🛠️ ປັບປຸງ: ຕັດ 'timestamp' ອອກ ແລ້ວແທນທີ່ດ້ວຍ SchoolYearFilter ທີ່ເຮົາສ້າງໄວ້ດ້ານເທິງ ✅
    list_filter = (SchoolYearFilter, 'province1', 'chinese_level', 'is_graduated_m7')

    list_display_links = ('full_name', 'organization')
    list_per_page = 20

    # ຟັງຊັນສຳລັບຄຳນວນ ແລະ ສ້າງລຳດັບ 1, 2, 3... (ໂຄດເດີມຂອງທ່ານ)
    def row_number(self, obj):
        if hasattr(self, '_row_counter'):
            self._row_counter += 1
        else:
            try:
                page = int(self.request.GET.get('p', 0))
            except ValueError:
                page = 0
            self._row_counter = (page * self.list_per_page) + 1
        return self._row_counter
    row_number.short_description = 'ລຳດັບ (No.)'

    def changelist_view(self, request, extra_context=None):
        self.request = request
        if hasattr(self, '_row_counter'):
            delattr(self, '_row_counter')
        return super().changelist_view(request, extra_context=extra_context)

    # ຟັງຊັນສຳລັບດຶງຊື່ວິຊາ (ໂຄດເດີມຂອງທ່ານ)
    def display_subjects(self, obj):
        subjects = obj.subject_set.all()
        if subjects.exists():
            return ", ".join([subject.name for subject in subjects])
        return "-"
    display_subjects.short_description = 'ວິຊາທີ່ເລືອກ (选择课程)'

    # ຟັງຊັນສຳລັບສ້າງຮູບພາບຕົວຢ່າງ Thumbnail (ໂຄດເດີມຂອງທ່ານ)
    def show_image(self, obj):
        if obj.image:
            img_html = format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px; cursor: pointer;" onclick="openImagePopup(this.src)" />', 
                obj.image.url
            )
            popup_html = """
            <div id="imageModal" style="display:none; position:fixed; z-index:9999; left:0; top:0; width:100%; height:100%; background-color:rgba(0,0,0,0.8); align-items:center; justify-content:center;">
                <span onclick="closeImagePopup()" style="position:absolute; top:20px; right:35px; color:#fff; font-size:40px; font-weight:bold; cursor:pointer;">&times;</span>
                <img id="modalImage" style="max-width:80%; max-height:80%; border-radius:8px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
            </div>
            <script>
            if (typeof openImagePopup !== 'function') {
                function openImagePopup(src) {
                    var modal = document.getElementById("imageModal");
                    var modalImg = document.getElementById("modalImage");
                    if (modal && modalImg) {
                        modal.style.display = "flex";
                        modalImg.src = src;
                    }
                }
                function closeImagePopup() {
                    var modal = document.getElementById("imageModal");
                    if (modal) {
                        modal.style.display = "none";
                    }
                }
                window.onclick = function(event) {
                    var modal = document.getElementById("imageModal");
                    if (event.target == modal) {
                        modal.style.display = "none";
                    }
                }
            }
            </script>
            """
            return mark_safe(f"{img_html}{popup_html}")
        return format_html('<span style="color: #999;">{}</span>', 'ບໍ່ມີຮູບ')
    show_image.short_description = 'ຮູບພາບ'