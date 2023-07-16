from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.core.validators import EmailValidator
from django_countries.fields import CountryField
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
#lista
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
    def create_superuser(self,username,correou,nombreu,apellidou,fechanacu,password,ciudadu,sexou,paisu):
        Usuario = self.create_user(
            username = username,
            correou = correou,
            nombreu = nombreu,
            apellidou = apellidou,
            fechanacu = fechanacu,
            password = password,
            ciudadu = ciudadu,
            sexou = sexou,
            paisu = paisu
        )
        Usuario.is_admin = True
        Usuario.save()
        return Usuario
    
    #lista
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
    es_admin = models.BooleanField(default=False)
    u_activo = models.BooleanField(default=True)
    sub_fk = models.ForeignKey(Suscripcion, models.DO_NOTHING,null=True,blank=True)
    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nombreu','apellidou','fechanacu','correou','password','ciudadu','sexou','paisu']

    def __str__(self):
        return self.idu + ' - ' + self.correou
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.es_admin
    
    @property
    def is_superuser(self):
        return self.es_admin

    class Meta:
        managed = False
        db_table =u'"infousuarios\".\"usuario"'

#lista
class Perfil(models.Model):
    per_id = models.AutoField(primary_key=True)
    idioma = models.CharField(max_length=10)
    percorreo = models.CharField()
    esta_activo = models.BooleanField(default=False)
    fk_usuario = models.ForeignKey(Usuario, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table =u'"infousuarios\".\"perfil"'
#lista
class Actividad(models.Model):
    act_id = models.AutoField(primary_key=True)
    act_ingreso = models.DateTimeField()
    act_dispositivo = models.CharField(max_length=30)
    act_fin = models.DateTimeField()
    fk_perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table =u'"infousuarios\".\"actividad"'
#lista
class Beneficio(models.Model):
    benid = models.AutoField(primary_key=True)
    bendescripcion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table =u'"infousuarios\".\"beneficio"'


#lista
class SuscripcionBeneficio(models.Model):
    fk_ben_sus = models.ForeignKey(Beneficio, models.DO_NOTHING,primary_key=True)  
    fk_sus_ben = models.ForeignKey(Suscripcion, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table =u'"infousuarios\".\"suscripcion_beneficio"'
        unique_together = (('fk_ben_sus', 'fk_sus_ben'),)

#lista
class Tarjetacredito(models.Model):
    tdcnumero = models.BigIntegerField('Numero de la tarjeta',primary_key=True,blank=False,null=False)
    tdcfecvencimiento = models.DateField('Fecha de vencimiento de la tarjeta',blank=False,null=False)
    tdccvv = models.IntegerField('Codigo de seguridad de la tarjeta',blank=False,null=False, validators=[MaxValueValidator(999), MinValueValidator(100)])
    fk_usuario = models.OneToOneField(Usuario, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table =u'"infousuarios\".\"tarjetacredito"'
#lista
class Personaje(models.Model):
    personaje_id = models.AutoField(primary_key=True)
    genc = models.CharField('Sexo del personaje',null=False,blank=False,choices=[('M','Masculino'),('F','Femenino'),('Desc','Desconocido'),('Otro','Otro')])
    primer_nombre = models.CharField('Primer nombre del personaje',max_length=20)
    segundo_nombre = models.CharField('Segundo nombre del personaje',max_length=20, blank=True, null=True)
    primer_apellido = models.CharField('Primer apellido del personaje',max_length=20)
    segundo_apellido = models.CharField('Segundo apellido del personaje',max_length=20, blank=True, null=True)
    color_pelo = models.CharField('Color del pelo del personaje',max_length=15)
    color_ojos = models.CharField('Color de los ojos del personaje',max_length=15)
    frase_celebre = models.CharField('Frase más celebre del personaje',max_length=75, blank=True, null=True)
    comic_primer_vez = models.CharField('Primera aparición en comics del personaje',max_length=50)
    estadomarital = models.CharField('Estado Marital del personaje',choices=[('Casado','Casado'),('Soltero','Soltero'),('Viudo','Viudo'),('Divorciado','Divorciado')])

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"personaje"'
    
    def __str__(self):
        return f"{self.personaje_id} - {self.primer_nombre} {self.primer_apellido}"
#lista
class Civil(models.Model):
    personaje = models.OneToOneField(Personaje, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"civil"'
    def __str__(self):
        return f"{self.personaje.personaje_id} - {self.personaje.primer_nombre} {self.personaje.primer_apellido}"
#lista
class Amistad(models.Model):
    id = models.AutoField(primary_key=True)
    civil = models.ForeignKey(Civil, models.DO_NOTHING)  
    amispers = models.ForeignKey(Personaje, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"amistad"'
        unique_together = (('civil', 'amispers'),)


#lista
class Combate(models.Model):
    cmbid = models.AutoField(primary_key=True)
    cmblugar = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"combate"'

    def __str__(self):
        return f"Combate Nro {self.cmbid}"
#FALTA
class Creador(models.Model):
    id_creador = models.AutoField(primary_key=True)
    personaje_id_cre = models.ForeignKey(Personaje, models.DO_NOTHING)  
    creador_nombre = models.CharField(max_length=20)
    creador_apellido = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"creador"'
        unique_together = (('personaje_id_cre', 'id_creador'),)

#lista
class Heroe(models.Model):
    personaje = models.OneToOneField(Personaje, models.DO_NOTHING, primary_key=True)
    nombre_superheroe = models.CharField(max_length=20)
    color_traje = models.CharField(max_length=15)
    logotipo = models.CharField(max_length=75)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"heroe"'

    def __str__(self):
        return f"{self.personaje.personaje_id} - {self.nombre_superheroe}"

#lista
class HistoricoMatrimonio(models.Model):
    id = models.AutoField(primary_key=True)
    id_pers_conyug1 = models.ForeignKey(Personaje, models.DO_NOTHING) 
    id_pers_conyug2 = models.ForeignKey(Civil, models.DO_NOTHING,)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"historico_matrimonio"'
        unique_together = (('id_pers_conyug1', 'id_pers_conyug2', 'fecha_inicio'),)
#lista
class Organizacion(models.Model):
    id_organizacion = models.AutoField(primary_key=True)
    org_nombre = models.CharField('Nombre de la organizacion',max_length=40)
    eslogan = models.CharField('Eslogan de la organizacion',max_length=100)
    tipo_organizacion = models.CharField('Tipo de organizacion',choices=[('Malvada','Malvada'),('Civil','Civil'),('Heroica','Heroica')])
    comic_primer_vez = models.CharField('Primera aparicion en comics de la organizacion',max_length=30)
    objetivo_principal = models.CharField('Objetivo principal de la organizacion',max_length=70)
    lugar_creacion = models.CharField('Lugar de creacion de la organizacion',max_length=20)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"organizacion"'
        
    def __str__(self):
        return f"{self.id_organizacion} - {self.org_nombre}"
#lista
class HistoricoPersonaje(models.Model):
    id = models.AutoField(primary_key=True)
    fk_pers_org = models.ForeignKey(Personaje, models.DO_NOTHING) 
    fk_org_pers = models.ForeignKey(Organizacion, models.DO_NOTHING, blank=False, null=False)
    fundador = models.BooleanField('¿Fundó la organización?')
    lider = models.BooleanField('¿Lideró la organización?')
    fecha_union = models.DateField('Fecha de unión a la organización', blank=False, null=False)
    fecha_salida = models.DateField('Fecha de salida de la organización',blank=True, null=True)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"historico_personaje"'
        unique_together = (('fk_pers_org', 'fk_org_pers', 'fecha_union'),)
#lista
class Medio(models.Model):
    medio_id = models.AutoField(primary_key=True)
    medfecestreno = models.DateField('Fecha de estreno',null=False,blank=False)
    medcomcreacion = models.CharField('Creador',max_length=20)
    medcomproduc = models.CharField('Productor',max_length=40)
    medrating = models.IntegerField('Rating',choices=[(1,"1-Mala"),(2,"2-Mediocre"),(3,"3-Regular"),(4,"4-Buena"),(5,"5-Excelente")])
    medsinopsis = models.CharField('Sinopsis',max_length=300)
    medionombre = models.CharField('Nombre del medio',max_length=50, blank=False, null=False)
    tipomed = models.CharField('Tipo de medio',choices=[('Pelicula','Película'),('Serie','Serie'),('Juego','Juego')])

    class Meta:
        managed = False
        db_table = 'medio'

    def __str__(self):
        return f"{self.medionombre}"
#lista
class Jueplataforma(models.Model):
    id_plataforma = models.AutoField(primary_key=True)
    plataforma = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"jueplataforma"'

    def __str__(self):
        return f"{self.id_plataforma} - {self.plataforma}"
#lista
class Juego(models.Model):
    medio = models.OneToOneField(Medio, models.DO_NOTHING, primary_key=True)
    medtipo = models.CharField('Tipo de Juego',choices=[('accion','accion'),('aventura','aventura'),('estrategia','estrategia'),('rpg','rpg'),('mundo abierto','mundo abierto'),('simulacion','simulacion')])
    juegocompania = models.CharField('Compañia desarrolladora',max_length=20)
    fk_plataforma = models.ForeignKey(Jueplataforma, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"juego"'

#lista
class Nacionalidad(models.Model):
    id_nacion = models.AutoField(primary_key=True)
    personaje_id_nac = models.ForeignKey(Personaje, models.DO_NOTHING) 
    nacion_nombre = models.CharField('Nombre del pais',max_length=20)
    nacion_continente = models.CharField('Continente de la nación',choices=[('America','America'),('Europa','Europa'),('Africa','Africa'),('Asia','Asia'),('Oceania','Oceania')])

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"nacionalidad"'
        unique_together = (('personaje_id_nac', 'id_nacion'),)
#lista
class Tipoobj(models.Model):
    idtipo = models.AutoField(primary_key=True)
    tipo_nombre = models.CharField(max_length=20)
    tipo_descripcion = models.CharField(max_length=70)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"tipoobj"'

    def __str__(self):
        return f"{self.idtipo} - {self.tipo_nombre}"
#lista
class Objeto(models.Model):
    obid = models.AutoField(primary_key=True)
    objnombre = models.CharField('Nombre del Objeto',max_length=50)
    objmaterial = models.CharField('Material del Objeto',max_length=20)
    objdescripcion = models.CharField('Descripción del Objeto',max_length=70)
    objtipo = models.ForeignKey(Tipoobj, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"objeto"'

    def __str__(self):
        return f"{self.obid} - {self.objnombre}"

#FALTA
class Ocupacion(models.Model):
    id_ocupacion = models.AutoField(primary_key=True)
    personaje_id_ocu = models.ForeignKey(Personaje, models.DO_NOTHING)
    ocupa_nombre = models.CharField('Ocupación del personaje',max_length=20)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"ocupacion"'
        unique_together = (('personaje_id_ocu', 'id_ocupacion'),)
#lista
class OrganizacionMedio(models.Model):
    id = models.AutoField(primary_key=True)
    fk_med_org = models.ForeignKey(Medio, models.DO_NOTHING) 
    fk_org_med = models.ForeignKey(Organizacion, models.DO_NOTHING)
    estado = models.CharField('Estado de la organización',choices=[('Desconocido','Desconocido'),('Activa','Activa'),('Inactiva','Inactiva'),('Disuelta','Disuelta')])

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"organizacion_medio"'
        unique_together = (('fk_med_org', 'fk_org_med'),)

#lista
class Pelicula(models.Model):
    medio = models.OneToOneField(Medio, models.DO_NOTHING, primary_key=True)
    medtipo = models.CharField('Tipo de pelicula',choices=[('animada','animada'),('liveaction','liveaction'),('stopmotion','stopmotion')],max_length=20)
    peldirector = models.CharField('Director de la pelicula',max_length=40)
    pelduracion = models.IntegerField('Duracion de la pelicula')
    pelcosteprod = models.DecimalField('Coste de produccion',max_digits=10, decimal_places=2)
    pelganancias = models.DecimalField('Ganancias de la pelicula',max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"pelicula"'        
#lista
class PerfilMedio(models.Model):
    id = models.AutoField(primary_key=True)
    fk_perf_med = models.ForeignKey(Perfil, models.DO_NOTHING)  
    fk_med_perf = models.ForeignKey(Medio, models.DO_NOTHING)
    calificacion = models.IntegerField('Calificacion del medio del perfil',choices=[(1,"1-Mala"),(2,"2-Mediocre"),(3,"3-Regular"),(4,"4-Buena"),(5,"5-Excelente")],default=1)
    fecha_vista = models.DateTimeField()

    class Meta:
        managed = False
        db_table =u'"infousuarios\".\"perfil_medio"'
        unique_together = (('fk_perf_med', 'fk_med_perf'),)

#lista
class PersonajeMedio(models.Model):
    id = models.AutoField(primary_key=True)
    fk_med_pers = models.ForeignKey(Medio, models.DO_NOTHING)  
    fk_pers_med = models.ForeignKey(Personaje, models.DO_NOTHING)
    actor_tipo = models.CharField('Rol del actor',choices=[('Interpreta','Interpreta'),('Presta su voz','Presta su voz')])
    actor_nombre = models.CharField('Nombre del Actor',max_length=40,null=False,blank=False)
    personaje_tipo = models.CharField('Rol del Personaje',choices=[('Antagonista','Antagonista'),('Protagonista','Protagonista'),('Secundario','Secundario')])

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"personaje_medio"'
        unique_together = (('fk_med_pers', 'fk_pers_med'),)

#lista
class PersonajeObjeto(models.Model):
    id = models.AutoField(primary_key=True)
    fk_obj_pers = models.ForeignKey(Objeto, models.DO_NOTHING) 
    fk_pers_obj = models.ForeignKey(Personaje, models.DO_NOTHING)
    hereditario = models.BooleanField()

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"personaje_objeto"'
        unique_together = (('fk_obj_pers', 'fk_pers_obj'),)

#lista
class Poder(models.Model):
    podid = models.AutoField(primary_key=True)
    ponombre = models.CharField('Nombre del Poder',max_length=30)
    podescripcion = models.CharField('Descripción del Poder',max_length=70)
    ponaturaleza = models.CharField('Naturaleza del Poder',max_length=20)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"poder"'
    
    def __str__(self):
        return f"{self.podid} - {self.ponombre}"

#lista
class PersonajePoder(models.Model):
    id = models.AutoField(primary_key=True)
    fk_pod_pers = models.OneToOneField(Poder, models.DO_NOTHING,related_name='Poder',)  
    fk_pers_pod = models.ForeignKey(Personaje, models.DO_NOTHING,related_name='Personaje')
    hereditario = models.BooleanField('¿Es heredado?')

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"personaje_poder"'
        unique_together = (('fk_pod_pers', 'fk_pers_pod'),)


#lista
class RegistroCombates(models.Model):
    id = models.AutoField(primary_key=True)
    fk_cmb_reg = models.ForeignKey(Combate, models.DO_NOTHING)
    fk_obj_reg = models.ForeignKey(Objeto, models.DO_NOTHING)
    id_pers_reg = models.ForeignKey(Personaje, models.DO_NOTHING)
    id_pod_reg = models.ForeignKey(Poder, models.DO_NOTHING)
    cmbfecha = models.DateField("Fecha de Combate")

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"registro_combates"'
        unique_together = (('fk_cmb_reg', 'fk_obj_reg', 'id_pers_reg', 'id_pod_reg', 'cmbfecha'),)

#lista
class Sede(models.Model):
    id_sede = models.AutoField(primary_key=True)
    sede_nombre = models.CharField('Nombre de la sede',max_length=20)
    sede_ubicacion = models.CharField('Ubicación de la sede',max_length=20)
    tipo_edificacion = models.CharField('Tipo de edificacion de la sede',choices=[('Subterranea','Subterranea'),('voladora','voladora'),('Superficial','Superficial')])
    org = models.ForeignKey(Organizacion, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"sede"'

#lista
class Serie(models.Model):
    medio = models.OneToOneField(Medio, models.DO_NOTHING, primary_key=True)
    medtipo = models.CharField('Tipo de serie',choices=[('animada','animada'),('liveaction','liveaction'),('stopmotion','stopmotion')])
    sercreador = models.CharField('Creador de la serie',max_length=40)
    serepisodios = models.IntegerField('Episodios de la serie')
    sercanal = models.CharField('Canal de transmision de la serie',max_length=20)

    class Meta:
        managed = False
        db_table = 'serie'
#lista
class Villano(models.Model):
    personaje = models.OneToOneField(Personaje, models.DO_NOTHING, primary_key=True)
    nombre_supervillano = models.CharField('nombre de villano',max_length=20)
    objetivo = models.CharField('Objetivo del villano',max_length=50)
    archienemigo = models.OneToOneField(Heroe, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table =u'"infopersonajes\".\"villano"'

