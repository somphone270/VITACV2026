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
    list_display = ['name', 'is_premium', 'price', 'photo', 'description', 'promotion_end_at']
    search_fields = ['name']

# Register
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Subject, SubjectAdmin)

admin.site.register(MyModel, fields=('my_image_thumbnail',), readonly_fields=('my_image_thumbnail',))


@admin.register(FormResponse)
class FormResponseAdmin(admin.ModelAdmin):
    # 1. ກໍານົດຄໍລຳທີ່ຈະໃຫ້ສະແດງຢູ່ໜ້າຕາຕະລາງລວມ
    list_display = (
        'id',
        'show_image',        # ສະແດງຮູບພາບຕົວຢ່າງ
        'full_name',         # ຊື່ ແລະ ນາມສະກຸນ
        'name_Chinese',
        'organization',      # ມາຈາກພາກສ່ວນ/ໂຮງຮຽນ
        'district',          # ເມືອງ
        'province1',     # ແຂວງ
        'is_graduated_m7',  
        'current_grade',
        'display_subjects',  # 🔥 ເພີ່ມຟີວນີ້ເພື່ອສະແດງວິຊາທີ່ເລືອກ
        'chinese_level',     # ລະດັບພາສາຈີນ
        'phone_number', # ເບີຕິດຕໍ່
        'facebook' ,   
        'timestamp'          # ເວລາບັນທຶກ
    )

    # 2. ເພີ່ມແຖບຄົ້ນຫາ (Search) ໂດຍອ້າງອີງຈາກ ຊື່, ໂຮງຮຽນ ຫຼື ເບີໂທ
    search_fields = ('full_name', 'organization', 'phone_number', 'district', 'province1')
 
    # 3. ເພີ່ມແຖບໂຕຕອງຂໍ້ມູນ (Filter) ຢູ່ດ້ານຂວາມື
    list_filter = ('province1', 'chinese_level', 'is_graduated_m7', 'timestamp')

    # 4. ກໍານົດໃຫ້ສາມາດກົດເຂົ້າໄປແກ້ໄຂຂໍ້ມູນໄດ້ໂດຍຄລິກທີ່ ຊື່ ຫຼື ໂຮງຮຽນ
    list_display_links = ('full_name', 'organization')

    # 5. ກໍານົດຈໍານວນຂໍ້ມູນທີ່ຈະສະແດງຕໍ່ 1 ໜ້າ (ຕົວຢ່າງ: 20 ແຖວ)
    list_per_page = 20
     # 🔥 6. ເພີ່ມຟັງຊັນສຳລັບດຶງຊື່ວິຊາທັງໝົດທີ່ຖືກຕິກເລືອກອອກມາສະແດງ
    def display_subjects(self, obj):
        # ດຶງຊື່ວິຊາທັງໝົດມາເຊື່ອມກັນດ້ວຍເຄື່ອງໝາຍຈຸດ (, ) 
        # ຖ້າບໍ່ມີການເລືອກວິຊາ ຈະສະແດງເຄື່ອງໝາຍ -
        subjects = obj.subject_set.all()
        if subjects.exists():
            return ", ".join([subject.name for subject in subjects])
        return "-"
         # 2. ເພີ່ມແຖວນີ້ເຂົ້າໄປເພື່ອປ່ຽນຊື່ຫົວຂໍ້ (Header) ເປັນພາສາລາວ
     # ຕັ້ງຊື່ຫົວຄໍລຳທີ່ຈະໄປສະແດງໃນໜ້າຕາຕະລາງ Admin
    display_subjects.short_description = 'ວິຊາທີ່ເລືອກ (选择课程)'
    # 6. ຟັງຊັນສຳລັບສ້າງຮູບພາບຕົວຢ່າງ (Thumbnail) ສະແດງໃນຕາຕະລາງ
     

    def show_image(self, obj):
        if obj.image:
            # 1. ສ້າງແທັກຮູບພາບຂະໜາດນ້ອຍ
            img_html = format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px; cursor: pointer;" onclick="openImagePopup(this.src)" />',
                obj.image.url
            )
            
            # 2. ສ້າງໂຄ້ດ Popup HTML & JavaScript
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
                    if (modal && modalImg) { modal.style.display = "flex"; modalImg.src = src; }
                }
                function closeImagePopup() {
                    var modal = document.getElementById("imageModal");
                    if (modal) { modal.style.display = "none"; }
                }
                window.onclick = function(event) {
                    var modal = document.getElementById("imageModal");
                    if (event.target == modal) { modal.style.display = "none"; }
                }
            }
            </script>
            """
            from django.utils.safestring import mark_safe
            return mark_safe(f"{img_html}{popup_html}")
            
        return format_html('<span style="color: #999;">{}</span>', 'ບໍ່ມີຮູບ')

    show_image.short_description = 'ຮູບພາບ'

    