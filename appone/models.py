from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.core.validators import EmailValidator
from django_countries.fields import CountryField
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Suscripcion(models.Model):
    susid = models.AutoField(primary_key=True)
    sustipo = models.CharField(max_length=10)
    susdescripcion = models.CharField(max_length=50)
    sustarifa = models.DecimalField(max_digits=5, decimal_places=4)

    class Meta:
        managed = False
        db_table =u'"infousuarios\".\"suscripcion"'


class UsuarioManager(BaseUserManager):
    def create_user(self,username,correou,nombreu,apellidou,fechanacu,password,ciudadu,sexou,paisu):
        if not correou:
            raise ValueError('El usuario debe tener correo electronico')
        Usuario = self.model(
            username = username,
            correou = self.normalize_email(correou),
            nombreu = nombreu,
            apellidou = apellidou,
            fechanacu = fechanacu,
            password = password,
            ciudadu = ciudadu,
            sexou = sexou,
            paisu = paisu
        )
        Usuario.set_password(password)
        Usuario.save()
        return Usuario

class Usuario(AbstractBaseUser):
    username = models.CharField('Identificador del usuario',primary_key=True, max_length=15)
    nombreu = models.CharField('Nombre del usuario',null=False,blank=False,max_length=20)
    apellidou = models.CharField('Apellido del usuario',null=False,blank=False,max_length=20)
    fechanacu = models.DateField('Fecha de nacimiento del usuario',null=False,blank=False)
    correou = models.CharField('Correo electronico',unique=True,null=False,blank=False, max_length=50)
    password = models.CharField('Contraseña del usuario',null=False,blank=False,max_length=20)
    ciudadu = models.CharField('Ciudad del usuario',null=False,blank=False,max_length=30)
    sexou = models.CharField('Sexo del usuario',null=False,blank=False,choices=[('M','Masculino'),('F','Femenino'),('Desc','Desconocido'),('Otro','Otro')],max_length=10)
    paisu = CountryField('Pais del usuario',null=False,blank=False,max_length=15)
    sub_fk = models.ForeignKey(Suscripcion, models.DO_NOTHING,null=True,blank=True)
    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nombreu','apellidou','fechanacu','correou','password','ciudadu','sexou','paisu']

    def __str__(self):
        return self.idu + ' - ' + self.correou

    class Meta:
        managed = False
        db_table =u'"infousuarios\".\"usuario"'

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
    fk_usuario = models.ForeignKey(Usuario, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table =u'"infousuarios\".\"perfil"'

class Actividad(models.Model):
    act_id = models.AutoField(primary_key=True)
    act_ingreso = models.DateTimeField()
    act_dispositivo = models.CharField(max_length=10)
    act_fin = models.DateTimeField()
    fk_perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table =u'"infousuarios\".\"actividad"'

class Beneficio(models.Model):
    benid = models.AutoField(primary_key=True)
    bendescripcion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table =u'"infousuarios\".\"beneficio"'



class SuscripcionBeneficio(models.Model):
    fk_ben_sus = models.ForeignKey(Beneficio, models.DO_NOTHING,primary_key=True)  
    fk_sus_ben = models.ForeignKey(Suscripcion, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table =u'"infousuarios\".\"suscripcion_beneficio"'
        unique_together = (('fk_ben_sus', 'fk_sus_ben'),)


class Tarjetacredito(models.Model):
    tdcnumero = models.BigIntegerField('Numero de la tarjeta',primary_key=True,blank=False,null=False)
    tdcfecvencimiento = models.DateField('Fecha de vencimiento de la tarjeta',blank=False,null=False)
    tdccvv = models.IntegerField('Codigo de seguridad de la tarjeta',blank=False,null=False, validators=[MaxValueValidator(999), MinValueValidator(100)])
    fk_usuario = models.OneToOneField(Usuario, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table =u'"infousuarios\".\"tarjetacredito"'

class Personaje(models.Model):
    id_personaje = models.IntegerField(primary_key=True)
    genC = models.CharField('Sexo del personaje',null=False,blank=False,choices=[('M','Masculino'),('F','Femenino'),('Desc','Desconocido'),('Otro','Otro')])
    primer_nombre = models.CharField('Primer nombre del personaje',max_length=20)
    segundo_nombre = models.CharField('Segundo nombre del personaje',max_length=20)
    primer_apellido = models.CharField('Primer apellido del personaje',max_length=20)
    segundo_apellido = models.CharField('Segundo apellido del personaje',max_length=20)
    color_pelo = models.CharField('Color del pelo del personaje',max_length=15)
    color_ojos = models.CharField('Color de los ojos del personaje',max_length=15)
    frase_celebre = models.CharField('Frase más celebre del personaje',max_length=75, blank=True, null=True)
    comic_primer_vez = models.CharField('Primera aparición en comics del personaje',max_length=50)
    estadomarital = models.CharField('Estado Marital del personaje',choices=[('Casado','Casado'),('Soltero','Soltero'),('Viudo','Viudo'),('Divorciado','Divorciado')])

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"personaje"'

class Civil(models.Model):
    id_personaje = models.OneToOneField(Personaje, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"civil"'


class Amistad(models.Model):
    id_civil = models.OneToOneField(Civil, models.DO_NOTHING,primary_key=True)  
    id_amispers = models.ForeignKey(Personaje, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"amistad"'
        unique_together = (('id_civil', 'id_amispers'),)



class Combate(models.Model):
    cmbid = models.AutoField(primary_key=True)
    cmblugar = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"combate"'


class Creador(models.Model):
    id_personaje_cre = models.OneToOneField(Personaje, models.DO_NOTHING, primary_key=True)  
    id_creador = models.IntegerField()
    creador_nombre = models.CharField(max_length=20)
    creador_apellido = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"creador"'
        unique_together = (('id_personaje_cre', 'id_creador'),)


class Heroe(models.Model):
    id_personaje = models.OneToOneField(Personaje, models.DO_NOTHING, primary_key=True)
    nombre_superheroe = models.CharField(max_length=20)
    color_traje = models.CharField(max_length=15)
    logotipo = models.CharField(max_length=75)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"heroe"'


class HistoricoMatrimonio(models.Model):
    id_pers_conyug1 = models.ForeignKey(Personaje, models.DO_NOTHING, primary_key=True) 
    id_pers_conyug2 = models.ForeignKey(Civil, models.DO_NOTHING,)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"historico_matrimonio"'
        unique_together = (('id_pers_conyug1', 'id_pers_conyug2', 'fecha_inicio'),)

class Organizacion(models.Model):
    id_organizacion = models.AutoField(primary_key=True)
    org_nombre = models.CharField(max_length=40)
    eslogan = models.CharField(max_length=100)
    tipo_organizacion = models.CharField(choices=[('Malvada','Malvada'),('Civil','Civil'),('Heroica','Heroica')])
    comic_primer_vez = models.CharField(max_length=30)
    objetivo_principal = models.CharField(max_length=70)
    lugar_creacion = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"organizacion"'

class HistoricoPersonaje(models.Model):
    fk_pers_org = models.ForeignKey(Personaje, models.DO_NOTHING, primary_key=True) 
    fk_org_pers = models.OneToOneField(Organizacion, models.DO_NOTHING, blank=True, null=True)
    fundador = models.BooleanField()
    lider = models.BooleanField()
    fecha_union = models.DateField()
    fecha_salida = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"historico_personaje"'
        unique_together = (('fk_pers_org', 'fk_org_pers', 'fecha_union'),)

class Medio(models.Model):
    medio_id = models.AutoField(primary_key=True)
    medfecestreno = models.DateField()
    medcomcreacion = models.CharField(max_length=20)
    medcomproduc = models.CharField(max_length=40)
    medrating = models.IntegerField(choices=[(1,"1-Mala"),(2,"2-Mediocre"),(3,"3-Regular"),(4,"4-Buena"),(5,"3-Excelente")])
    medsinopsis = models.CharField(max_length=120)

    class Meta:
        managed = False
        db_table = 'medio'

class Jueplataforma(models.Model):
    id_plataforma = models.AutoField(primary_key=True)
    plataforma = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"jueplataforma"'

class Juego(models.Model):
    medio = models.OneToOneField(Medio, models.DO_NOTHING, primary_key=True)
    medtipo = models.CharField(choices=[('accion','accion'),('aventura','aventura'),('estrategia','estrategia'),('rpg','rpg'),('mundo abierto','mundo abierto'),('simulacion','simulacion')])
    juegocompania = models.CharField(max_length=20)
    fk_plataforma = models.ForeignKey(Jueplataforma, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"juego"'


class Nacionalidad(models.Model):
    id_personaje_nac = models.OneToOneField(Personaje, models.DO_NOTHING, primary_key=True) 
    id_nacion = models.IntegerField()
    nacion_nombre = models.CharField(max_length=20)
    nacion_continente = models.CharField(choices=[('America','America'),('Europa','Europa'),('Africa','Africa'),('Asia','Asia'),('Oceania','Oceania')])

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"nacionalidad"'
        unique_together = (('id_personaje_nac', 'id_nacion'),)

class Tipoobj(models.Model):
    idtipo = models.AutoField(primary_key=True)
    tipo_nombre = models.CharField(max_length=20)
    tipo_descripcion = models.CharField(max_length=70)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"tipoobj"'

class Objeto(models.Model):
    obid = models.AutoField(primary_key=True)
    objnombre = models.CharField(max_length=20)
    objmaterial = models.CharField(max_length=20)
    objdescripcion = models.CharField(max_length=70)
    objtipo = models.ForeignKey(Tipoobj, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"objeto"'


class Ocupacion(models.Model):
    id_personaje_ocu = models.OneToOneField(Personaje, models.DO_NOTHING, primary_key=True)
    id_ocupacion = models.IntegerField()
    ocupa_nombre = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"ocupacion"'
        unique_together = (('id_personaje_ocu', 'id_ocupacion'),)

class OrganizacionMedio(models.Model):
    fk_med_org = models.OneToOneField(Medio, models.DO_NOTHING, primary_key=True) 
    fk_org_med = models.ForeignKey(Organizacion, models.DO_NOTHING)
    estado = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"organizacion_medio"'
        unique_together = (('fk_med_org', 'fk_org_med'),)


class Pelicula(models.Model):
    medio = models.OneToOneField(Medio, models.DO_NOTHING, primary_key=True)
    medtipo = models.CharField(choices=[('animada','animada'),('liveaction','liveaction'),('stopmotion','stopmotion')])
    peldirector = models.CharField(max_length=40)
    pelduracion = models.IntegerField()
    pelcosteprod = models.DecimalField(max_digits=5, decimal_places=4)
    pelganancias = models.DecimalField(max_digits=5, decimal_places=4)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"pelicula"'        

class PerfilMedio(models.Model):
    fk_perf_med = models.OneToOneField(Perfil, models.DO_NOTHING, primary_key=True)  
    fk_med_perf = models.OneToOneField(Medio, models.DO_NOTHING)
    calificacion = models.IntegerField()
    fecha_vista = models.DateTimeField()

    class Meta:
        managed = False
        db_table =u'"infousuarios\".\"perfil_medio"'
        unique_together = (('fk_perf_med', 'fk_med_perf'),)


class PersonajeMedio(models.Model):
    fk_med_pers = models.OneToOneField(Medio, models.DO_NOTHING,primary_key=True)  
    fk_pers_med = models.ForeignKey(Personaje, models.DO_NOTHING)
    actor_tipo = models.CharField()
    actor_nombre = models.CharField(max_length=40)
    personaje_tipo = models.CharField(choices=[('Antagonista','Antagonista'),('Protagonista','Protagonista'),('Secundario','Secundario')])

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"personaje_medio"'
        unique_together = (('fk_med_pers', 'fk_pers_med'),)


class PersonajeObjeto(models.Model):
    fk_obj_pers = models.OneToOneField(Objeto, models.DO_NOTHING, primary_key=True) 
    fk_pers_obj = models.ForeignKey(Personaje, models.DO_NOTHING)
    hereditario = models.BooleanField()

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"personaje_objeto"'
        unique_together = (('fk_obj_pers', 'fk_pers_obj'),)


class PersonajePoder(models.Model):
    fk_pod_pers = models.OneToOneField('Poder', models.DO_NOTHING, primary_key=True)  
    fk_pers_pod = models.ForeignKey(Personaje, models.DO_NOTHING)
    hereditario = models.BooleanField()

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"personaje_poder"'
        unique_together = (('fk_pod_pers', 'fk_pers_pod'),)


class Poder(models.Model):
    podid = models.AutoField(primary_key=True)
    ponombre = models.CharField(max_length=30)
    podescripcion = models.CharField(max_length=70)
    ponaturaleza = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"poder"'


class RegistroCombates(models.Model):
    fk_cmb_reg = models.ForeignKey(Combate, models.DO_NOTHING,primary_key=True)
    fk_obj_reg = models.ForeignKey(Objeto, models.DO_NOTHING)
    id_pers_reg = models.ForeignKey(Personaje, models.DO_NOTHING)
    id_pod_reg = models.ForeignKey(Poder, models.DO_NOTHING)
    cmbfecha = models.DateField()

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"registro_combates"'
        unique_together = (('fk_cmb_reg', 'fk_obj_reg', 'id_pers_reg', 'id_pod_reg', 'cmbfecha'),)


class Sede(models.Model):
    id_sede = models.AutoField(primary_key=True)
    sede_nombre = models.CharField(max_length=20)
    sede_ubicacion = models.CharField(max_length=20)
    tipo_edificacion = models.CharField(choices=[('Subterranea','Subterranea'),('voladora','voladora'),('Superficial','Superficial')])
    id_org = models.OneToOneField(Organizacion, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"sede"'


class Serie(models.Model):
    medio = models.OneToOneField(Medio, models.DO_NOTHING, primary_key=True)
    medtipo = models.CharField(choices=[('animada','animada'),('liveaction','liveaction'),('stopmotion','stopmotion')])
    sercreador = models.CharField(max_length=40)
    serepisodios = models.IntegerField()
    sercanal = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'serie'

class Villano(models.Model):
    id_personaje = models.OneToOneField(Personaje, models.DO_NOTHING, primary_key=True)
    nombre_supervillano = models.CharField(max_length=20)
    objetivo = models.CharField(max_length=50)
    archienemigo = models.OneToOneField(Heroe, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"villano"'

