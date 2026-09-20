from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor


ROOT = Path(r"C:\Users\Juan\AndroidStudioProjects\iudigitalradioapp")
OUTPUT = ROOT / "output" / "docx" / "Guia_Edwin_Ruiz_feature_hardware.docx"

BLACK = "000000"
DARK_BLUE = "17365D"
WHITE = "FFFFFF"
LIGHT_GRAY = "D9D9D9"
PALE_GRAY = "F5F6F8"
ALT_ROW = "F2F5F9"


def set_font(run, name="Aptos", size=11, bold=False, color=BLACK, italic=False):
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), name)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor.from_string(color)


def shade(cell, fill):
    props = cell._tc.get_or_add_tcPr()
    node = props.find(qn("w:shd"))
    if node is None:
        node = OxmlElement("w:shd")
        props.append(node)
    node.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=78, start=125, bottom=78, end=125):
    props = cell._tc.get_or_add_tcPr()
    margins = props.first_child_found_in("w:tcMar")
    if margins is None:
        margins = OxmlElement("w:tcMar")
        props.append(margins)
    for side, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        element = margins.find(qn(f"w:{side}"))
        if element is None:
            element = OxmlElement(f"w:{side}")
            margins.append(element)
        element.set(qn("w:w"), str(value))
        element.set(qn("w:type"), "dxa")


def set_table_borders(table):
    props = table._tbl.tblPr
    borders = props.find(qn("w:tblBorders"))
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        props.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = borders.find(qn(f"w:{edge}"))
        if tag is None:
            tag = OxmlElement(f"w:{edge}")
            borders.append(tag)
        tag.set(qn("w:val"), "single")
        tag.set(qn("w:sz"), "6")
        tag.set(qn("w:color"), LIGHT_GRAY)


def set_repeat_header(row):
    props = row._tr.get_or_add_trPr()
    repeat = OxmlElement("w:tblHeader")
    repeat.set(qn("w:val"), "true")
    props.append(repeat)


def prevent_row_split(row):
    row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))


def set_cell_text(cell, text, bold=False, color=BLACK, size=9.2, center=False):
    cell.text = ""
    paragraph = cell.paragraphs[0]
    paragraph.paragraph_format.space_after = Pt(0)
    paragraph.paragraph_format.line_spacing = 1.02
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.LEFT
    run = paragraph.add_run(str(text))
    set_font(run, size=size, bold=bold, color=color)
    set_cell_margins(cell)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def add_table(doc, headers, rows, widths=None, centered_columns=None):
    centered_columns = centered_columns or set()
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table)
    header = table.rows[0]
    set_repeat_header(header)
    prevent_row_split(header)
    for index, label in enumerate(headers):
        shade(header.cells[index], DARK_BLUE)
        set_cell_text(header.cells[index], label, bold=True, color=WHITE, size=9.2,
                      center=index in centered_columns)
        if widths:
            header.cells[index].width = widths[index]
    for row_index, values in enumerate(rows):
        row = table.add_row()
        prevent_row_split(row)
        for index, value in enumerate(values):
            if row_index % 2 == 1:
                shade(row.cells[index], ALT_ROW)
            set_cell_text(row.cells[index], value, size=8.9, center=index in centered_columns)
            if widths:
                row.cells[index].width = widths[index]
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(0)
    return table


def add_body(doc, text, bold_prefix=None):
    paragraph = doc.add_paragraph(style="Body Text")
    if bold_prefix and text.startswith(bold_prefix):
        first = paragraph.add_run(bold_prefix)
        set_font(first, bold=True)
        rest = paragraph.add_run(text[len(bold_prefix):])
        set_font(rest)
    else:
        set_font(paragraph.add_run(text))
    return paragraph


def add_bullets(doc, items):
    for item in items:
        paragraph = doc.add_paragraph(style="List Bullet")
        set_font(paragraph.add_run(item), size=10.5)


def add_steps(doc, items, start=1):
    for number, item in enumerate(items, start=start):
        paragraph = doc.add_paragraph(style="Body Text")
        paragraph.paragraph_format.left_indent = Cm(0.72)
        paragraph.paragraph_format.first_line_indent = Cm(-0.72)
        set_font(paragraph.add_run(f"{number}.  "), bold=True)
        set_font(paragraph.add_run(item))


def add_code(doc, code):
    paragraph = doc.add_paragraph(style="Code Block")
    paragraph.paragraph_format.left_indent = Cm(0.25)
    paragraph.paragraph_format.right_indent = Cm(0.25)
    paragraph.paragraph_format.space_before = Pt(3)
    paragraph.paragraph_format.space_after = Pt(8)
    paragraph.paragraph_format.line_spacing = 1.0
    props = paragraph._p.get_or_add_pPr()
    node = OxmlElement("w:shd")
    node.set(qn("w:fill"), PALE_GRAY)
    props.append(node)
    lines = code.rstrip().splitlines() or [""]
    for index, line in enumerate(lines):
        run = paragraph.add_run(line)
        set_font(run, name="Consolas", size=6.9, color="202020")
        if index < len(lines) - 1:
            run.add_break()


def add_note(doc, label, text):
    paragraph = doc.add_paragraph(style="Body Text")
    paragraph.paragraph_format.space_before = Pt(4)
    set_font(paragraph.add_run(label + " "), bold=True)
    set_font(paragraph.add_run(text))


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = paragraph.add_run("Página ")
    set_font(run, size=8)
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instruction = OxmlElement("w:instrText")
    instruction.set(qn("xml:space"), "preserve")
    instruction.text = "PAGE"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.extend([begin, instruction, end])


def add_file_section(doc, number, title, relative_path, purpose, explanations, page_break=True):
    if page_break:
        doc.add_page_break()
    doc.add_heading(f"{number} {title}", level=1)
    add_body(doc, f"Ruta: {relative_path}", bold_prefix="Ruta:")
    add_body(doc, purpose)
    doc.add_heading("Qué hace cada parte", level=2)
    add_bullets(doc, explanations)
    doc.add_heading("Código que debe quedar", level=2)
    source = (ROOT / relative_path).read_text(encoding="utf-8")
    add_code(doc, source)


doc = Document()
section = doc.sections[0]
section.page_width = Inches(8.5)
section.page_height = Inches(11)
section.top_margin = Cm(1.8)
section.bottom_margin = Cm(1.7)
section.left_margin = Cm(2.0)
section.right_margin = Cm(2.0)
section.header_distance = Cm(0.8)
section.footer_distance = Cm(0.8)

styles = doc.styles
for style_name, size in (("Normal", 11), ("Body Text", 11)):
    styles[style_name].font.name = "Aptos"
    styles[style_name].font.size = Pt(size)
    styles[style_name].font.color.rgb = RGBColor.from_string(BLACK)
    styles[style_name].paragraph_format.space_after = Pt(7)
    styles[style_name].paragraph_format.line_spacing = 1.1
for style_name in ("List Bullet", "List Number"):
    styles[style_name].font.name = "Aptos"
    styles[style_name].font.size = Pt(10.5)
    styles[style_name].font.color.rgb = RGBColor.from_string(BLACK)
    styles[style_name].paragraph_format.space_after = Pt(4)

styles["Title"].font.name = "Aptos Display"
styles["Title"].font.size = Pt(28)
styles["Title"].font.bold = True
styles["Title"].font.color.rgb = RGBColor.from_string(BLACK)
styles["Title"].paragraph_format.space_after = Pt(10)
styles["Title"].paragraph_format.keep_with_next = True
title_props = styles["Title"].element.get_or_add_pPr()
title_border = title_props.find(qn("w:pBdr"))
if title_border is not None:
    title_props.remove(title_border)

for level, size in ((1, 20), (2, 14), (3, 12)):
    style = styles[f"Heading {level}"]
    style.font.name = "Aptos Display"
    style.font.size = Pt(size)
    style.font.bold = True
    style.font.color.rgb = RGBColor.from_string(BLACK)
    style.paragraph_format.space_before = Pt(14 if level == 1 else 10)
    style.paragraph_format.space_after = Pt(6)
    style.paragraph_format.keep_with_next = True

if "Code Block" not in styles:
    code_style = styles.add_style("Code Block", WD_STYLE_TYPE.PARAGRAPH)
else:
    code_style = styles["Code Block"]
code_style.font.name = "Consolas"
code_style.font.size = Pt(6.9)
code_style.font.color.rgb = RGBColor.from_string("202020")

header = section.header.paragraphs[0]
header.text = "IU DIGITAL RADIO   GUÍA DE TRABAJO POR RAMA"
header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
for run in header.runs:
    set_font(run, size=8, bold=True)
add_page_number(section.footer.paragraphs[0])

# Portada
doc.add_paragraph().paragraph_format.space_before = Pt(48)
title = doc.add_paragraph(style="Title")
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_font(title.add_run("Guía de implementación de cámara, permisos y vibración"),
         name="Aptos Display", size=28, bold=True)
subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_font(subtitle.add_run("Evidencia de aprendizaje 3 · Aplicación móvil Android IU Digital Radio"),
         size=13, bold=True)
role = doc.add_paragraph()
role.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_font(role.add_run("Trabajo individual del rol simulado de Edwin Ruiz"), size=11, italic=True)
doc.add_paragraph()
add_table(
    doc,
    ["Dato", "Valor"],
    [
        ("Integrante", "Edwin Ruiz"),
        ("Rama asignada", "feature/hardware"),
        ("Responsabilidad", "Cámara, permiso en tiempo de ejecución, vibración y pruebas de hardware"),
        ("Base recibida", "main con el estado y la interfaz principal ya integrados"),
        ("Commit local verificado", "37ede2d · Integra cámara permisos y vibración"),
        ("Estado", "Implementado, compilado y validado funcionalmente"),
        ("Fecha de la guía", "17 de septiembre de 2026"),
    ],
    widths=[Cm(4.2), Cm(11.8)],
)
add_note(doc, "Propósito.", "Que Edwin pueda reproducir, comprender, probar y explicar su aporte sin depender de memorizar el código.")

doc.add_page_break()
doc.add_heading("1. Resultado que debe entregar Edwin", level=1)
add_body(doc, "Al finalizar, la aplicación debe solicitar el permiso de cámara cuando sea necesario, abrir la cámara del dispositivo, mostrar la fotografía capturada en la interfaz y emitir una vibración de confirmación después de una captura válida.")
add_bullets(doc, [
    "La aplicación sigue funcionando si el dispositivo no tiene cámara; se muestra un mensaje explicativo.",
    "Si el usuario niega el permiso, la cámara no se abre y aparece un mensaje.",
    "Si el usuario cancela la captura, no se guarda una fotografía ni se produce la vibración.",
    "Si la captura es exitosa, el estado de Compose recibe el Bitmap, la fotografía se visualiza y luego se activa la confirmación háptica.",
    "El proyecto continúa compilando y las pruebas automatizadas verifican los permisos y la actualización del estado.",
])
add_note(doc, "Importante.", "La vibración real debe comprobarse en un teléfono físico. Algunos emuladores no exponen un servicio de vibrador, aunque el código y las pruebas sean correctos.")

doc.add_heading("2. Límite del trabajo de Edwin", level=1)
add_table(doc, ["Sí corresponde a Edwin", "No corresponde a Edwin"], [
    ("Declarar CAMERA y VIBRATE en el manifiesto.", "Rediseñar la pantalla principal de Juan Pablo."),
    ("Consultar y solicitar el permiso de cámara.", "Cambiar las reglas del reducer creadas para el estado."),
    ("Abrir la cámara y recibir la miniatura capturada.", "Implementar reproducción real de audio."),
    ("Activar la vibración tras una captura exitosa.", "Hacer la integración final de todas las ramas."),
    ("Crear pruebas instrumentadas de configuración.", "Subir directamente cambios a main sin revisión."),
], widths=[Cm(8), Cm(8)])
add_body(doc, "MainActivity usa temporalmente HardwareDemoRoute para que Edwin pueda ejecutar su módulo completo. En la integración final, Juan Ardila reemplazará ese coordinador provisional por RadioRoute y conservará la lógica probada.")

doc.add_heading("3. Archivos involucrados", level=1)
add_table(doc, ["Archivo", "Tipo", "Finalidad"], [
    ("AndroidManifest.xml", "Modificado", "Permisos y declaración opcional de cámara."),
    ("CameraPermission.kt", "Nuevo", "Nombre y comprobación del permiso CAMERA."),
    ("DeviceVibrator.kt", "Nuevo", "Confirmación háptica de una captura exitosa."),
    ("HardwareDemoRoute.kt", "Nuevo", "Coordinación provisional entre UI, permiso, cámara y vibrador."),
    ("MainActivity.kt", "Modificado", "Entrada temporal al coordinador de hardware."),
    ("HardwareConfigurationTest.kt", "Nuevo", "Pruebas instrumentadas de permisos y fotografía en el estado."),
], widths=[Cm(4.6), Cm(2.3), Cm(9.1)])

doc.add_page_break()
doc.add_heading("4. Preparar la rama correctamente", level=1)
add_body(doc, "Antes de crear archivos, Edwin debe recibir la última versión estable de main. Esto evita trabajar sobre una estructura antigua y reduce conflictos posteriores.")
add_steps(doc, [
    "Abrir el proyecto iudigitalradioapp en Android Studio.",
    "Abrir la terminal integrada en la carpeta raíz del proyecto.",
    "Cambiar a main y traer la versión remota más reciente.",
    "Cambiar a feature/hardware y combinar main dentro de esa rama.",
    "Verificar que la terminal muestre feature/hardware y que el proyecto compile antes de comenzar.",
])
add_code(doc, """git switch main
git pull origin main
git switch feature/hardware
git merge main
git status""")
add_note(doc, "Resultado esperado.", "Git debe indicar que Edwin está en feature/hardware. Si aparece un conflicto, no debe borrar archivos: debe avisar al coordinador y resolverlo comparando ambas versiones.")
doc.add_heading("Estructura que debe crear", level=2)
add_code(doc, """app/src/main/java/com/example/iudigitalradioapp/hardware/
├── CameraPermission.kt
├── DeviceVibrator.kt
└── HardwareDemoRoute.kt

app/src/androidTest/java/com/example/iudigitalradioapp/hardware/
└── HardwareConfigurationTest.kt""")
add_note(doc, "Cómo crear el package.", "En la vista Project de Android Studio, ubique java/com.example.iudigitalradioapp, haga clic derecho, seleccione New > Package y escriba hardware. Repita bajo androidTest para la prueba.")

add_file_section(
    doc, "5.", "Declarar permisos y disponibilidad de cámara",
    "app/src/main/AndroidManifest.xml",
    "El manifiesto informa a Android qué recursos de hardware utilizará la aplicación antes de que se ejecute.",
    [
        "CAMERA permite solicitar acceso a la cámara. Es un permiso peligroso y, por eso, también debe pedirse durante la ejecución.",
        "VIBRATE autoriza la vibración. No necesita un cuadro de permiso en tiempo de ejecución.",
        "uses-feature con required=false evita excluir de la instalación a equipos sin cámara.",
        "El comentario de responsabilidad permite identificar el aporte de Edwin durante la revisión académica.",
    ],
)
add_note(doc, "Evidencia recomendada.", "Captura del manifiesto mostrando las dos líneas uses-permission y el bloque uses-feature.")

add_file_section(
    doc, "6.", "Centralizar el permiso de cámara",
    "app/src/main/java/com/example/iudigitalradioapp/hardware/CameraPermission.kt",
    "Este objeto evita repetir el nombre del permiso y la consulta a ContextCompat en diferentes lugares.",
    [
        "object crea una única instancia reutilizable; no es necesario construirla con new.",
        "permission conserva Manifest.permission.CAMERA como una constante legible.",
        "isGranted(context) compara el resultado de checkSelfPermission con PERMISSION_GRANTED.",
        "La clase no abre la cámara: solamente responde si el permiso ya fue concedido.",
    ],
)
add_note(doc, "Cómo explicarlo.", "CameraPermission es una utilidad pequeña: concentra una responsabilidad y permite que HardwareDemoRoute tome la decisión correcta.")

add_file_section(
    doc, "7.", "Implementar la confirmación por vibración",
    "app/src/main/java/com/example/iudigitalradioapp/hardware/DeviceVibrator.kt",
    "Esta clase encapsula el acceso al servicio Vibrator y ofrece una función con un nombre relacionado con el caso de uso.",
    [
        "applicationContext evita conservar accidentalmente una Activity más tiempo del necesario.",
        "getSystemService(Vibrator::class.java) obtiene el servicio del dispositivo; puede ser null si el equipo no lo ofrece.",
        "confirmPhotoCaptured usa EFFECT_DOUBLE_CLICK, una señal corta de confirmación.",
        "El operador ?. evita un error si no existe servicio de vibración.",
        "La función se invoca únicamente después de recibir una fotografía no nula.",
    ],
)
add_note(doc, "Momento exacto de la vibración.", "Después de que la cámara devuelve un Bitmap válido y el reducer lo guarda en el estado. No vibra al abrir la cámara, pedir permiso, negar permiso ni cancelar la captura.")

add_file_section(
    doc, "8.", "Coordinar permiso, cámara, estado y vibración",
    "app/src/main/java/com/example/iudigitalradioapp/hardware/HardwareDemoRoute.kt",
    "HardwareDemoRoute es un composable provisional de integración. Conecta la pantalla existente con efectos del sistema Android.",
    [
        "LocalContext obtiene el Context necesario para permisos, funciones del sistema y mensajes Toast.",
        "remember conserva DeviceVibrator y el estado mientras Compose recompone la pantalla.",
        "TakePicturePreview abre una aplicación de cámara compatible y devuelve un Bitmap pequeño o null si se cancela.",
        "RequestPermission muestra el diálogo del sistema y comunica si el permiso fue concedido.",
        "requestCamera comprueba primero que exista cámara, después revisa el permiso y finalmente abre o solicita lo necesario.",
        "RadioAction.OpenCamera se trata como un efecto externo; las demás acciones siguen pasando por RadioReducer.",
        "PhotoCaptured(bitmap) actualiza el estado antes de activar la vibración.",
    ],
)
doc.add_heading("Flujo funcional", level=2)
add_code(doc, """Usuario pulsa Abrir cámara
        ↓
¿El dispositivo tiene cámara?
  ├─ No → mostrar mensaje y terminar
  └─ Sí
        ↓
¿CAMERA ya está concedido?
  ├─ No → solicitar permiso
  │        ├─ Negado → mostrar mensaje
  │        └─ Concedido → abrir cámara
  └─ Sí → abrir cámara
        ↓
¿La cámara devolvió una fotografía?
  ├─ No → informar cancelación
  └─ Sí → guardar Bitmap → mostrarlo → vibrar""")

add_file_section(
    doc, "9.", "Conectar temporalmente el módulo",
    "app/src/main/java/com/example/iudigitalradioapp/MainActivity.kt",
    "La Activity instala el tema de Compose y presenta HardwareDemoRoute para probar el aporte de Edwin de principio a fin.",
    [
        "setContent inicia la interfaz declarativa.",
        "IudigitalradioappTheme conserva los estilos del proyecto.",
        "HardwareDemoRoute es temporal; permite validar la rama sin esperar la integración final.",
        "El comentario deja explícito que Juan Ardila hará el reemplazo por RadioRoute.",
    ],
)
add_note(doc, "No confundir.", "Edwin no está apropiándose de la integración final. Esta conexión es una plataforma de prueba temporal y está documentada como tal.")

add_file_section(
    doc, "10.", "Crear las pruebas instrumentadas",
    "app/src/androidTest/java/com/example/iudigitalradioapp/hardware/HardwareConfigurationTest.kt",
    "Las pruebas instrumentadas se ejecutan en Android porque necesitan PackageManager y Bitmap reales del framework.",
    [
        "manifestDeclaresCameraAndVibrationPermissions inspecciona el paquete instalado y confirma que ambos permisos fueron solicitados.",
        "La condición por versión usa PackageInfoFlags en Android 13 o superior y conserva compatibilidad con versiones anteriores.",
        "capturedPhotoIsStoredInScreenState crea un Bitmap pequeño, envía PhotoCaptured al reducer y comprueba que se conserva la misma instancia.",
        "Estas pruebas no sustituyen la comprobación manual del diálogo, la cámara ni la vibración física.",
    ],
)

doc.add_heading("11. Ejecutar y probar manualmente", level=1)
doc.add_heading("11.1 Preparar la primera solicitud", level=2)
add_body(doc, "Si el permiso ya se había concedido, el cuadro de Android no volverá a aparecer. Para documentar el primer uso, se puede revocar desde Ajustes > Aplicaciones > IU Digital Radio > Permisos > Cámara > No permitir, y luego abrir otra vez la aplicación.")
add_note(doc, "Alternativa con ADB.", "Este comando es opcional y se ejecuta con un dispositivo o emulador conectado:")
add_code(doc, "adb shell pm revoke com.example.iudigitalradioapp android.permission.CAMERA")

doc.add_heading("11.2 Casos manuales", level=2)
add_table(doc, ["Caso", "Acción", "Resultado esperado"], [
    ("Permiso pendiente", "Pulsar Abrir cámara.", "Android solicita autorización para usar la cámara."),
    ("Permiso negado", "Seleccionar No permitir.", "La cámara no abre y aparece el mensaje explicativo."),
    ("Permiso concedido", "Autorizar y continuar.", "Se abre la aplicación de cámara disponible."),
    ("Captura cancelada", "Salir de la cámara sin aceptar foto.", "Se informa la cancelación; no hay foto nueva ni vibración."),
    ("Captura válida", "Tomar y aceptar una foto.", "La imagen aparece en la tarjeta y el teléfono vibra dos pulsos breves."),
    ("Sin cámara", "Ejecutar en un equipo que no la exponga.", "Se muestra que no hay cámara disponible sin cerrar la aplicación."),
], widths=[Cm(3.1), Cm(5.2), Cm(7.7)])
add_note(doc, "Prueba ya realizada.", "El flujo de cámara, permiso y actualización de la fotografía fue probado correctamente. La vibración debe registrarse desde un teléfono físico porque el emulador empleado no ofrece servicio de vibrador.")

doc.add_heading("12. Verificación técnica realizada", level=1)
add_body(doc, "Desde la raíz del proyecto se ejecutaron las siguientes tareas de Gradle:")
add_code(doc, r""".\gradlew.bat testDebugUnitTest assembleDebug compileDebugAndroidTestKotlin
.\gradlew.bat connectedDebugAndroidTest
.\gradlew.bat lintDebug""")
add_table(doc, ["Verificación", "Resultado"], [
    ("Pruebas unitarias", "12 aprobadas."),
    ("Pruebas instrumentadas", "6 aprobadas: 1 base, 3 de interfaz y 2 de hardware."),
    ("APK de depuración", "assembleDebug finalizó correctamente."),
    ("Compilación de androidTest", "compileDebugAndroidTestKotlin finalizó correctamente."),
    ("Análisis estático", "lintDebug finalizó con BUILD SUCCESSFUL."),
    ("Advertencias de lint", "15 no bloqueantes: dependencias disponibles, colores de plantilla sin usar y label redundante preexistente."),
], widths=[Cm(5), Cm(11)])
doc.add_page_break()
doc.add_heading("13. Revisar y crear el commit", level=1)
add_body(doc, "Edwin debe confirmar que su commit incluya solamente los archivos funcionales del módulo. Los directorios .idea, output y tmp no forman parte del aporte.")
add_code(doc, """git status
git diff -- app/src/main/AndroidManifest.xml
git diff -- app/src/main/java/com/example/iudigitalradioapp/MainActivity.kt
git diff -- app/src/main/java/com/example/iudigitalradioapp/hardware
git diff -- app/src/androidTest/java/com/example/iudigitalradioapp/hardware""")
add_body(doc, "Si el contenido es correcto, se agregan rutas explícitas para evitar subir archivos locales por accidente:")
add_code(doc, """git add app/src/main/AndroidManifest.xml
git add app/src/main/java/com/example/iudigitalradioapp/MainActivity.kt
git add app/src/main/java/com/example/iudigitalradioapp/hardware
git add app/src/androidTest/java/com/example/iudigitalradioapp/hardware
git commit -m "Integra cámara permisos y vibración"
git status""")
add_note(doc, "Commit local actual.", "La implementación validada quedó registrada como 37ede2d con el mensaje “Integra cámara permisos y vibración”.")

doc.add_heading("14. Publicar la rama y solicitar Pull Request", level=1)
add_steps(doc, [
    "Publicar feature/hardware en el repositorio remoto.",
    "Abrir GitHub y seleccionar Compare & pull request.",
    "Confirmar base: main y compare: feature/hardware.",
    "Escribir un resumen corto y las pruebas realizadas.",
    "Asignar la revisión a Juan Ardila, responsable de integración.",
    "Esperar aprobación antes de combinar; Edwin no debe hacer push directo a main.",
])
add_code(doc, "git push -u origin feature/hardware")
doc.add_heading("Texto sugerido para el Pull Request", level=2)
add_code(doc, """Título: Integra cámara, permisos y vibración

Resumen:
- declara CAMERA y VIBRATE en el manifiesto;
- solicita CAMERA durante la ejecución;
- abre la cámara con TakePicturePreview;
- muestra la captura en el estado de la pantalla;
- vibra después de una captura válida;
- agrega pruebas instrumentadas de configuración.

Validación:
- 12 pruebas unitarias aprobadas;
- 6 pruebas instrumentadas aprobadas;
- assembleDebug y lintDebug correctos;
- flujo manual de cámara probado.""")
add_note(doc, "Después del merge.", "Juan Ardila debe actualizar su main, ejecutar nuevamente las pruebas y sustituir HardwareDemoRoute por RadioRoute durante la integración general.")

doc.add_page_break()
doc.add_heading("15. Empaquetar una copia ZIP opcional", level=1)
add_body(doc, "GitHub y el Pull Request son la evidencia principal del trabajo colaborativo. Si el docente también solicita un ZIP, se debe generar sin carpetas temporales ni configuración local.")
add_steps(doc, [
    "Cerrar la aplicación si está ejecutándose, pero no es obligatorio cerrar Android Studio.",
    "En GitHub, abrir la rama feature/hardware y usar Code > Download ZIP; así solo se incluyen archivos rastreados.",
    "Renombrar el archivo como iudigitalradioapp-feature-hardware-Edwin-Ruiz.zip.",
    "Abrir el ZIP y verificar que contenga app, gradle, build.gradle.kts, settings.gradle.kts y gradlew.bat.",
])
add_note(doc, "No incluir.", ".idea, .gradle, build, output, tmp, archivos de emulador ni credenciales locales.")

doc.add_page_break()
doc.add_heading("16. Capturas numeradas para la evidencia", level=1)
add_body(doc, "Las capturas son evidencia de lo realizado y de que funciona. No necesitan registrar cada clic de creación. Deben verse claras, estar numeradas y llevar una explicación debajo.")
add_table(doc, ["N.º", "Captura", "Texto sugerido debajo"], [
    ("1", "Terminal en feature/hardware después de integrar main.", "Se preparó la rama individual a partir de la versión estable del equipo."),
    ("2", "Árbol de paquetes con la carpeta hardware y sus tres archivos.", "Se organizó el acceso a hardware en un package con responsabilidad definida."),
    ("3", "AndroidManifest.xml con CAMERA, VIBRATE y uses-feature.", "Se declararon permisos y se mantuvo opcional la disponibilidad de cámara."),
    ("4", "Código de CameraPermission y DeviceVibrator.", "Se centralizó la consulta del permiso y la confirmación háptica."),
    ("5", "Diálogo real de Android solicitando cámara.", "La aplicación solicita el permiso peligroso durante la ejecución."),
    ("6", "Aplicación de cámara abierta desde IU Digital Radio.", "Tras autorizar, el contrato de actividad inicia la captura."),
    ("7", "Pantalla mostrando la fotografía capturada.", "El Bitmap devuelto se almacenó en el estado y Compose actualizó la interfaz."),
    ("8", "Teléfono físico o nota de prueba de vibración.", "Después de aceptar la foto se emitió la confirmación de doble pulsación."),
    ("9", "Salida BUILD SUCCESSFUL de las pruebas.", "Las pruebas unitarias e instrumentadas finalizaron correctamente."),
    ("10", "Historial de Git con el commit de Edwin.", "El aporte quedó aislado en un commit identificable de feature/hardware."),
    ("11", "Pull Request feature/hardware → main.", "El trabajo se envió a revisión antes de integrarse a la rama principal."),
    ("12", "Pull Request aprobado o main actualizado.", "El coordinador revisó e incorporó el módulo al producto común."),
], widths=[Cm(1.2), Cm(6.6), Cm(8.2)], centered_columns={0})
add_note(doc, "Consejo de presentación.", "Recorte únicamente información ajena, conserve visible la rama o el nombre del archivo y no edite mensajes para aparentar resultados distintos de los obtenidos.")

doc.add_heading("17. Lista de comprobación de Edwin", level=1)
add_bullets(doc, [
    "□ Estoy ubicado en feature/hardware.",
    "□ AndroidManifest.xml declara CAMERA, VIBRATE y cámara opcional.",
    "□ CameraPermission.kt comprueba el permiso sin abrir la cámara.",
    "□ DeviceVibrator.kt vibra solamente tras una captura válida.",
    "□ HardwareDemoRoute.kt cubre cámara ausente, permiso, cancelación y éxito.",
    "□ MainActivity.kt se reconoce como conexión temporal.",
    "□ Las pruebas unitarias e instrumentadas terminan correctamente.",
    "□ Probé el flujo manual y registré capturas numeradas.",
    "□ Mi commit no incluye .idea, output, tmp ni carpetas build.",
    "□ Publiqué feature/hardware y abrí un Pull Request hacia main.",
])

doc.add_heading("18. Preguntas para sustentar el trabajo", level=1)
add_table(doc, ["Pregunta", "Respuesta breve esperada"], [
    ("¿Por qué CAMERA se pide durante la ejecución?", "Porque Android lo clasifica como permiso peligroso y el usuario debe decidir al momento de usar la función."),
    ("¿Por qué VIBRATE no muestra diálogo?", "Se concede al instalar; basta declararlo en el manifiesto."),
    ("¿Qué devuelve TakePicturePreview?", "Un Bitmap pequeño si la captura se acepta o null si se cancela."),
    ("¿Cuándo vibra la aplicación?", "Después de guardar en el estado una fotografía válida."),
    ("¿Qué ocurre si no hay cámara?", "Se muestra un Toast y la aplicación continúa abierta."),
    ("¿Por qué DeviceVibrator acepta Context?", "Para obtener el servicio Android sin acoplar la lógica directamente al composable."),
    ("¿Para qué sirve remember?", "Mantiene objetos y estado entre recomposiciones de Compose."),
    ("¿Por qué HardwareDemoRoute es provisional?", "Permite probar la rama; RadioRoute será el coordinador definitivo de todos los módulos."),
    ("¿Qué prueban las pruebas instrumentadas?", "Que el APK declara ambos permisos y que PhotoCaptured conserva el Bitmap en el estado."),
    ("¿Por qué usar Pull Request?", "Para revisar, documentar y combinar el aporte sin modificar main directamente."),
], widths=[Cm(6.4), Cm(9.6)])

doc.add_heading("19. Referencias", level=1)
add_body(doc, "Android Developers. (s. f.). Request runtime permissions. https://developer.android.com/training/permissions/requesting")
add_body(doc, "Android Developers. (s. f.). ActivityResultContracts.TakePicturePreview. https://developer.android.com/reference/androidx/activity/result/contract/ActivityResultContracts.TakePicturePreview")
add_body(doc, "Android Developers. (s. f.). Add haptic feedback to events. https://developer.android.com/develop/ui/views/haptics/haptic-feedback")
add_body(doc, "GitHub Docs. (s. f.). Creating a pull request. https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request")

doc.add_heading("20. Cierre", level=1)
add_body(doc, "El aporte de Edwin queda completo cuando el código está en feature/hardware, las pruebas pasan, el flujo manual está documentado y existe un Pull Request revisable hacia main. El objetivo no es solamente que la cámara se abra, sino poder explicar la relación entre permiso, contrato de actividad, estado de Compose y respuesta háptica.")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
doc.save(OUTPUT)
print(OUTPUT)
