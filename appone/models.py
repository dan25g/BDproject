from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.

class Usuario(AbstractBaseUser):
    idu = models.CharField('Identificador del usuario',primary_key=True, max_length=15)
    nombreu = models.CharField('Nombre del usuario',null=False,blank=False,max_length=20)
    apellidou = models.CharField('Apellido del usuario',null=False,blank=False,max_length=20)
    fechanacu = models.DateField('Fecha de nacimiento del usuario',null=False,blank=False)
    correou = models.CharField('Correo electronico',unique=True,null=False,blank=False, max_length=50)
    contrasennau = models.CharField('Contrasenna del usuario',null=False,blank=False,max_length=20)
    ciudadu = models.CharField('Ciudad del usuario',null=False,blank=False,max_length=10)
    sexou = models.CharField('Sexo del usuario',null=False,blank=False)
    paisu = models.CharField('Pais del usuario',null=False,blank=False,max_length=15)

    USERNAME_FIELD = 'idu'
    REQUIRED_FIELDS = ['nombreu','apellidou','fechanacu','correou','contrasennau','ciudadu','sexou','paisu']

    def __str__(self):
        return self.idu + ' - ' + self.correou

    class Meta:
        managed = False
        db_table = 'usuario'

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(Usuario,on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' - hecha por ' + self.user.username

class Perfil(models.Model):
    per_id = models.AutoField(primary_key=True)
    idioma = models.CharField(max_length=10)
    percorreo = models.CharField()
    fk_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='fk_usuario')

    class Meta:
        managed = False
        db_table = 'perfil'

class Actividad(models.Model):
    act_id = models.AutoField(primary_key=True)
    act_ingreso = models.DateTimeField()
    act_dispositivo = models.CharField(max_length=10)
    act_fin = models.DateTimeField()
    fk_perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, db_column='fk_perfil')

    class Meta:
        managed = False
        db_table = 'actividad'

class Beneficio(models.Model):
    benid = models.AutoField(primary_key=True)
    bendescripcion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'beneficio'





class Suscripcion(models.Model):
    susid = models.AutoField(primary_key=True)
    sustipo = models.CharField(max_length=10)
    susdescripcion = models.CharField(max_length=50)
    sustarifa = models.DecimalField(max_digits=5, decimal_places=4)

    class Meta:
        managed = False
        db_table = 'suscripcion'


class SuscripcionBeneficio(models.Model):
    fk_ben_sus = models.ForeignKey(Beneficio, models.DO_NOTHING, db_column='fk_ben_sus', primary_key=True)  # The composite primary key (fk_ben_sus, fk_sus_ben) found, that is not supported. The first column is selected.
    fk_sus_ben = models.ForeignKey(Suscripcion, models.DO_NOTHING, db_column='fk_sus_ben')

    class Meta:
        managed = False
        db_table = 'suscripcion_beneficio'
        unique_together = (('fk_ben_sus', 'fk_sus_ben'),)


class Tarjetacredito(models.Model):
    tdcnumero = models.AutoField(primary_key=True)
    tdcfecvencimiento = models.DateField()
    tdccvv = models.IntegerField()
    fk_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='fk_usuario')

    class Meta:
        managed = False
        db_table = 'tarjetacredito'


