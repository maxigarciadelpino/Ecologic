from django import forms
from .models import Profile

class ImagenPerfilForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        labels = {
            'image': 'Foto de perfil',
        }

def clean_image(self):
    imagen = self.cleaned_data.get('image')
    if imagen:
        # Validar extensión
        extension = imagen.name.split('.')[-1].lower()
        if extension not in ['jpg', 'jpeg', 'png']:
            raise forms.ValidationError('Solo se permiten archivos JPG o PNG.')
        
        # Validar tamaño de archivo
        if imagen.size > 5 * 1024 * 1024:  # límite de 5 MB
            raise forms.ValidationError('La imagen no debe superar los 5 MB.')
        
        # Validar dimensiones mínimas
        from PIL import Image
        img = Image.open(imagen)
        ancho, alto = img.size
        lado_minimo = min(ancho, alto)
        
        if lado_minimo < 256:
            raise forms.ValidationError(f'La imagen es muy pequeña. El lado más corto debe ser al menos 256px (actual: {lado_minimo}px).')
    
    return imagen
