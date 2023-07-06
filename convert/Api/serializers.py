from rest_framework import  serializers
from convert.models import Convert

class ConvertSerializers(serializers.ModelSerializer):
  
    id  = serializers.PrimaryKeyRelatedField(read_only = True)
    uploaded_file =serializers.FileField()
    exported_file = serializers.CharField(read_only = True)

    def create(self, validate_data):
        record = Convert(
            uploaded_file = validate_data['uploaded_file'],    
        )
        record.save()
        return record
    
    class Meta:
        model=Convert
        fields = ['id','exported_file','uploaded_file']