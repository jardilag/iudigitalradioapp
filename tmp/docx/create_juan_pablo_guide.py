from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor


ROOT = Path(r"C:\Users\Juan\AndroidStudioProjects\iudigitalradioapp")
OUTPUT = ROOT / "output" / "docx" / "Guia_Juan_Pablo_Gonzalez_feature_ui_compose.docx"
SCREENSHOT = ROOT / "tmp" / "ui" / "iudigitalradio_ui_grid.png"

BLACK = "000000"
DARK_BLUE = "17365D"
WHITE = "FFFFFF"
LIGHT_GRAY = "D9D9D9"
PALE_GRAY = "F5F6F8"
ALT_ROW = "F2F5F9"


def set_font(run, name="Aptos", size=11, bold=False, color=BLACK):
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), name)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = RGBColor.from_string(color)


def shade(cell, fill):
    props = cell._tc.get_or_add_tcPr()
    node = props.find(qn("w:shd"))
    if node is None:
        node = OxmlElement("w:shd")
        props.append(node)
    node.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=110, start=130, bottom=110, end=130):
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
    props = row._tr.get_or_add_trPr()
    props.append(OxmlElement("w:cantSplit"))


def set_cell_text(cell, text, bold=False, color=BLACK, size=9.5, center=False):
    cell.text = ""
    paragraph = cell.paragraphs[0]
    paragraph.paragraph_format.space_after = Pt(0)
    paragraph.paragraph_format.line_spacing = 1.05
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
        set_cell_text(header.cells[index], label, bold=True, color=WHITE, size=9.5, center=index in centered_columns)
        if widths:
            header.cells[index].width = widths[index]
    for row_index, values in enumerate(rows):
        row = table.add_row()
        prevent_row_split(row)
        for index, value in enumerate(values):
            if row_index % 2 == 1:
                shade(row.cells[index], ALT_ROW)
            set_cell_text(row.cells[index], value, size=9, center=index in centered_columns)
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
        run = paragraph.add_run(text)
        set_font(run)
    return paragraph


def add_bullets(doc, items):
    for item in items:
        paragraph = doc.add_paragraph(style="List Bullet")
        run = paragraph.add_run(item)
        set_font(run, size=10.5)


def add_steps(doc, items):
    for number, item in enumerate(items, start=1):
        paragraph = doc.add_paragraph(style="Body Text")
        paragraph.paragraph_format.left_indent = Cm(0.72)
        paragraph.paragraph_format.first_line_indent = Cm(-0.72)
        marker = paragraph.add_run(f"{number}.  ")
        set_font(marker, bold=True)
        text = paragraph.add_run(item)
        set_font(text)


def add_code(doc, code):
    paragraph = doc.add_paragraph(style="Code Block")
    paragraph.paragraph_format.left_indent = Cm(0.25)
    paragraph.paragraph_format.right_indent = Cm(0.25)
    paragraph.paragraph_format.space_before = Pt(3)
    paragraph.paragraph_format.space_after = Pt(8)
    paragraph.paragraph_format.line_spacing = 1.0
    props = paragraph._p.get_or_add_pPr()
    shade_node = OxmlElement("w:shd")
    shade_node.set(qn("w:fill"), PALE_GRAY)
    props.append(shade_node)
    lines = code.rstrip().splitlines() or [""]
    for index, line in enumerate(lines):
        run = paragraph.add_run(line)
        set_font(run, name="Consolas", size=8, color="202020")
        if index < len(lines) - 1:
            run.add_break()


def add_note(doc, label, text):
    paragraph = doc.add_paragraph(style="Body Text")
    paragraph.paragraph_format.space_before = Pt(4)
    first = paragraph.add_run(label + " ")
    set_font(first, bold=True)
    second = paragraph.add_run(text)
    set_font(second)


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


def add_file_section(doc, number, title, relative_path, purpose, points, page_break=False):
    if page_break:
        doc.add_page_break()
    doc.add_heading(f"{number} {title}", level=2)
    add_body(doc, f"Ruta {relative_path}", bold_prefix="Ruta ")
    add_body(doc, purpose)
    add_bullets(doc, points)
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
styles["Normal"].font.name = "Aptos"
styles["Normal"].font.size = Pt(11)
styles["Normal"].font.color.rgb = RGBColor.from_string(BLACK)
styles["Normal"].paragraph_format.space_after = Pt(6)
styles["Normal"].paragraph_format.line_spacing = 1.1

styles["Body Text"].font.name = "Aptos"
styles["Body Text"].font.size = Pt(11)
styles["Body Text"].font.color.rgb = RGBColor.from_string(BLACK)
styles["Body Text"].paragraph_format.space_after = Pt(7)
styles["Body Text"].paragraph_format.line_spacing = 1.1

for name in ("List Bullet", "List Number"):
    styles[name].font.name = "Aptos"
    styles[name].font.size = Pt(10.5)
    styles[name].font.color.rgb = RGBColor.from_string(BLACK)
    styles[name].paragraph_format.space_after = Pt(4)

styles["Title"].font.name = "Aptos Display"
styles["Title"].font.size = Pt(28)
styles["Title"].font.bold = True
styles["Title"].font.color.rgb = RGBColor.from_string(BLACK)
styles["Title"].paragraph_format.space_after = Pt(10)
styles["Title"].paragraph_format.keep_with_next = True
title_style_props = styles["Title"].element.get_or_add_pPr()
title_style_border = title_style_props.find(qn("w:pBdr"))
if title_style_border is not None:
    title_style_props.remove(title_style_border)

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
code_style.font.size = Pt(8)
code_style.font.color.rgb = RGBColor.from_string("202020")

header = section.header.paragraphs[0]
header.text = "IU DIGITAL RADIO   GUÍA DE TRABAJO POR RAMA"
header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
for run in header.runs:
    set_font(run, size=8, bold=True)
add_page_number(section.footer.paragraphs[0])

# Portada
doc.add_paragraph().paragraph_format.space_before = Pt(52)
title = doc.add_paragraph(style="Title")
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title.add_run("Guía de implementación de la interfaz principal con Jetpack Compose")
title_props = title._p.get_or_add_pPr()
title_border = title_props.find(qn("w:pBdr"))
if title_border is not None:
    title_props.remove(title_border)

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitle.add_run("IU Digital Radio")
set_font(run, size=16, bold=True)

description = doc.add_paragraph()
description.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = description.add_run("Procedimiento de desarrollo verificación publicación e integración")
set_font(run, size=12)

doc.add_paragraph("\n")
add_table(doc, ["Dato", "Asignación"], [
    ("Responsable", "Juan Pablo Gonzalez"),
    ("Rama", "feature/ui-compose"),
    ("Módulo", "Pantalla principal y componentes declarativos"),
    ("Punto de partida", "main actualizado con los contratos de estado"),
    ("Integración", "Pull Request desde feature/ui-compose hacia main"),
    ("Verificación", "12 pruebas unitarias y 4 pruebas instrumentadas aprobadas"),
    ("Versión de la guía", date.today().strftime("%d/%m/%Y")),
], widths=[Cm(4.0), Cm(11.6)])
add_note(doc, "Uso de la guía", "Juan Pablo debe ejecutar, revisar y explicar cada paso. La imagen del resultado esperado sirve como referencia y no sustituye las capturas tomadas durante su propio trabajo.")

doc.add_page_break()
doc.add_heading("1 Objetivo del módulo", level=1)
add_body(doc, "Juan Pablo construye la interfaz principal de IU Digital Radio con Jetpack Compose. La pantalla recibe RadioUiState, representa sus valores y convierte cada interacción del usuario en una RadioAction. Esta separación permite que la interfaz se pruebe antes de conectar la cámara, la vibración y el reproductor de audio.")
add_bullets(doc, [
    "Crear una pantalla desplazable que funcione en teléfonos.",
    "Mostrar la emisora seleccionada y el estado de reproducción.",
    "Mostrar las cinco emisoras en dos columnas sin desplazamiento horizontal.",
    "Permitir seleccionar emisoras y emitir acciones de reproducción y silencio.",
    "Reservar un panel para mostrar la fotografía recibida desde el módulo de cámara.",
    "Definir una paleta y tipografía consistentes en ui.theme.",
    "Comprobar la interfaz con una vista previa y pruebas instrumentadas.",
])

doc.add_heading("2 Responsabilidad de Juan Pablo", level=1)
add_table(doc, ["Corresponde a Juan Pablo", "Corresponde a otros módulos"], [
    ("RadioScreen y sus componentes Compose.", "Catálogo y reglas de estado de Luisa Gomez."),
    ("Presentación de botones y emisoras.", "Reproducción real con Media3 de Jorge Echavarría."),
    ("Panel visual de la fotografía.", "Permisos cámara y vibración de Edwin Ruiz."),
    ("Paleta tipografía tema y vista previa.", "RadioRoute e integración final de Juan Ardila."),
    ("Pruebas instrumentadas de la interfaz.", "Documentación final y control de calidad de Yeison Padron."),
])
add_note(doc, "Límite técnico", "Los componentes de Juan Pablo emiten acciones. No solicitan permisos, no abren la cámara y no reproducen una transmisión.")

doc.add_heading("3 Diferencia entre ui y ui theme", level=1)
add_body(doc, "El paquete ui contiene pantallas, componentes y contratos relacionados con lo que se muestra y con las acciones del usuario. El subpaquete ui.theme contiene colores, tipografía y configuración visual reutilizable. Theme no es otra pantalla; define el aspecto compartido por todas las pantallas.")
add_table(doc, ["Paquete", "Contenido"], [
    ("ui", "RadioScreen RadioScreenDemo RadioUiState RadioAction y RadioReducer."),
    ("ui/components", "StationSelector PlaybackControls y PhotoPanel."),
    ("ui/theme", "Color Theme y Type."),
])

doc.add_heading("4 Preparación desde main", level=1)
add_body(doc, "La guía comienza con main actualizado. Juan Pablo no debe recoger directamente la rama de otro integrante. Recibe los cambios aprobados desde main y los incorpora a feature/ui-compose.")
add_steps(doc, [
    "Abrir la terminal en la carpeta raíz que contiene gradlew.bat y settings.gradle.kts.",
    "Cambiar a main y descargar su versión más reciente.",
    "Cambiar a feature/ui-compose.",
    "Fusionar main dentro de feature/ui-compose.",
    "Confirmar que la rama activa sea feature/ui-compose y compilar antes de editar.",
])
add_code(doc, "git switch main\ngit pull origin main\ngit switch feature/ui-compose\ngit merge main\ngit branch --show-current\n\n$env:JAVA_HOME = \"C:\\Program Files\\Android\\Android Studio\\jbr\"\n.\\gradlew.bat assembleDebug")
add_note(doc, "Resultado esperado", "La terminal muestra feature/ui-compose y BUILD SUCCESSFUL. Si la rama sólo se trabajará localmente durante la práctica, git merge main utiliza el main local ya preparado.")

doc.add_heading("5 Mapa de archivos", level=1)
add_table(doc, ["Archivo", "Tipo de cambio", "Finalidad"], [
    ("MainActivity.kt", "Modificar", "Mostrar la ruta de demostración."),
    ("ui/RadioScreenDemo.kt", "Crear", "Mantener estado temporal para revisar la interfaz."),
    ("ui/RadioScreen.kt", "Crear", "Componer la pantalla principal."),
    ("ui/components/StationSelector.kt", "Crear", "Mostrar las cinco emisoras en dos columnas."),
    ("ui/components/PlaybackControls.kt", "Crear", "Mostrar controles de reproducción y silencio."),
    ("ui/components/PhotoPanel.kt", "Crear", "Mostrar el espacio y la foto de cámara."),
    ("ui/theme/Color.kt", "Modificar", "Definir la paleta visual."),
    ("ui/theme/Theme.kt", "Modificar", "Aplicar esquemas claro y oscuro."),
    ("ui/theme/Type.kt", "Modificar", "Definir jerarquía tipográfica."),
    ("RadioScreenTest.kt", "Crear", "Verificar contenido e interacción."),
], widths=[Cm(6.3), Cm(2.3), Cm(7.0)])

doc.add_page_break()
doc.add_heading("6 Implementación paso a paso", level=1)
add_body(doc, "Las rutas siguientes parten de la raíz del proyecto. El código mostrado coincide con el esqueleto compilado y probado en feature/ui-compose.")

add_file_section(doc, "6.1", "Conexión provisional en MainActivity", "app/src/main/java/com/example/iudigitalradioapp/MainActivity.kt", "MainActivity elimina la pantalla Hello Android y muestra RadioScreenDemo dentro del tema. La conexión está documentada como provisional porque Juan Ardila incorporará RadioRoute cuando existan los módulos de hardware y audio.", [
    "setContent inicia la composición declarativa.",
    "IudigitalradioappTheme aplica colores y tipografía.",
    "RadioScreenDemo permite ejecutar la interfaz sin implementar efectos externos.",
])

add_file_section(doc, "6.2", "Estado de demostración", "app/src/main/java/com/example/iudigitalradioapp/ui/RadioScreenDemo.kt", "RadioScreenDemo conserva un RadioUiState con remember y procesa las acciones mediante RadioReducer. Esta función permite comprobar las interacciones visuales mientras RadioRoute todavía no existe.", [
    "mutableStateOf vuelve observable el estado para Compose.",
    "El operador by permite leer y asignar state directamente.",
    "Cada acción produce un estado nuevo sin abrir cámara ni reproducir audio.",
], page_break=True)

add_file_section(doc, "6.3", "Pantalla principal", "app/src/main/java/com/example/iudigitalradioapp/ui/RadioScreen.kt", "RadioScreen es una función sin estado propio. Recibe el estado completo y una función onAction. LazyColumn permite desplazar el contenido en pantallas pequeñas.", [
    "Scaffold aplica correctamente el espacio del sistema.",
    "RadioHeader y SelectedStationCard resumen el estado actual.",
    "Los componentes secundarios reciben sólo los datos y eventos que necesitan.",
    "La vista previa usa datos reales del repositorio sin ejecutar la aplicación.",
], page_break=True)

add_file_section(doc, "6.4", "Selector de emisoras", "app/src/main/java/com/example/iudigitalradioapp/ui/components/StationSelector.kt", "StationSelector distribuye el catálogo en filas de dos columnas. Cada FilterChip compara su id con selectedStationId y devuelve el identificador elegido. La quinta emisora queda centrada con el ancho de una columna.", [
    "chunked(2) divide la lista en grupos de dos emisoras.",
    "Column y Row muestran todas las opciones sin desplazamiento horizontal.",
    "StationChip evita repetir la construcción y el evento de cada FilterChip.",
    "El componente muestra un mensaje cuando la lista está vacía.",
    "No modifica StationRepository ni conoce RadioReducer.",
], page_break=True)

add_file_section(doc, "6.5", "Controles de reproducción", "app/src/main/java/com/example/iudigitalradioapp/ui/components/PlaybackControls.kt", "PlaybackControls adapta el texto de sus botones al estado recibido. Los botones se deshabilitan si no existe una emisora seleccionada.", [
    "El botón principal alterna entre Reproducir y Pausar.",
    "El botón tonal alterna entre Silenciar y Activar sonido.",
    "Los callbacks comunican intención sin depender de Media3.",
])

add_file_section(doc, "6.6", "Panel de fotografía", "app/src/main/java/com/example/iudigitalradioapp/ui/components/PhotoPanel.kt", "PhotoPanel muestra un espacio informativo cuando no existe fotografía y representa el Bitmap cuando el estado contiene una captura.", [
    "aspectRatio mantiene el área visual estable.",
    "ContentScale.Crop adapta la fotografía al contenedor.",
    "Abrir cámara sólo ejecuta onOpenCamera; Edwin implementará el efecto real.",
])

add_file_section(doc, "6.7", "Paleta de colores", "app/src/main/java/com/example/iudigitalradioapp/ui/theme/Color.kt", "Color.kt reemplaza los colores de plantilla por una paleta azul naranja y neutra apropiada para la interfaz de radio.", [
    "Los nombres describen la función visual del color.",
    "Se incluyen superficies claras y oscuras.",
])

add_file_section(doc, "6.8", "Tema de la aplicación", "app/src/main/java/com/example/iudigitalradioapp/ui/theme/Theme.kt", "Theme.kt relaciona la paleta con los roles de Material 3. El color dinámico permanece desactivado para que las capturas se vean iguales en distintos dispositivos.", [
    "LightColorScheme define la apariencia normal.",
    "DarkColorScheme conserva contraste en modo oscuro.",
    "MaterialTheme entrega el esquema y la tipografía a toda la composición.",
], page_break=True)

add_file_section(doc, "6.9", "Tipografía", "app/src/main/java/com/example/iudigitalradioapp/ui/theme/Type.kt", "Type.kt define tamaños y pesos para encabezados títulos cuerpo y etiquetas. Los componentes consumen estos estilos mediante MaterialTheme.typography.", [
    "headlineMedium se usa en el nombre de la aplicación.",
    "titleLarge y titleMedium ordenan la información de las secciones.",
    "labelMedium se usa en el indicador de estado.",
])

add_file_section(doc, "6.10", "Pruebas de interfaz", "app/src/androidTest/java/com/example/iudigitalradioapp/ui/RadioScreenTest.kt", "RadioScreenTest abre MainActivity en un emulador. Una prueba verifica el contenido principal, otra comprueba que las cinco emisoras estén visibles sin desplazamiento horizontal y la tercera pulsa Reproducir para confirmar el cambio a Pausar y EN REPRODUCCIÓN.", [
    "createAndroidComposeRule inicia la actividad real.",
    "onNodeWithText localiza elementos por su semántica.",
    "assertCountEquals controla el nombre repetido de la emisora seleccionada.",
    "performClick reproduce una interacción del usuario.",
], page_break=True)

doc.add_page_break()
doc.add_heading("7 Resultado esperado", level=1)
add_body(doc, "La aplicación debe mostrar la emisora seleccionada, las cinco opciones en una cuadrícula de dos columnas, los controles y el panel de fotografía. No se requiere un gesto horizontal para descubrir emisoras. El contenido general puede desplazarse verticalmente para mantener accesible el botón de cámara.")
if SCREENSHOT.exists():
    paragraph = doc.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.add_run().add_picture(str(SCREENSHOT), width=Inches(3.15))
    caption = doc.add_paragraph()
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = caption.add_run("Figura 1  Resultado esperado del esqueleto Compose en un emulador Pixel 4 XL")
    set_font(run, size=9)
add_note(doc, "Importante", "Esta figura es una referencia de revisión. Juan Pablo debe tomar sus propias capturas mientras crea ejecuta y explica la interfaz.")

doc.add_heading("8 Verificación técnica", level=1)
add_body(doc, "La verificación se realiza en tres niveles. Primero se compila la aplicación y las pruebas. Después se ejecutan las pruebas unitarias. Por último se ejecutan las pruebas Compose en un emulador o dispositivo conectado.")
add_code(doc, "$env:JAVA_HOME = \"C:\\Program Files\\Android\\Android Studio\\jbr\"\n.\\gradlew.bat testDebugUnitTest assembleDebug compileDebugAndroidTestKotlin")
add_body(doc, "Con el emulador iniciado y desbloqueado:")
add_code(doc, ".\\gradlew.bat connectedDebugAndroidTest")
add_note(doc, "Resultado verificado", "BUILD SUCCESSFUL. Se aprobaron 12 pruebas unitarias y 4 pruebas instrumentadas: 3 de RadioScreenTest y 1 prueba base del proyecto.")

doc.add_heading("8.1 Solución cuando no aparece la jerarquía Compose", level=2)
add_body(doc, "Si el informe muestra No compose hierarchies found in the app, comprobar primero que el emulador esté encendido y desbloqueado. En la verificación local el fallo se produjo mientras el emulador estaba dormido y desapareció al despertarlo.")
add_code(doc, "adb devices\nadb shell input keyevent KEYCODE_WAKEUP\nadb shell wm dismiss-keyguard\n.\\gradlew.bat connectedDebugAndroidTest")

doc.add_heading("9 Revisión y commit local", level=1)
add_body(doc, "Juan Pablo debe revisar sólo sus archivos. No debe agregar .idea/misc.xml output tmp ni otros archivos locales. Se usan rutas específicas en lugar de git add punto.")
add_code(doc, "git status --short --branch\ngit diff --check\n\ngit add app/src/main/java/com/example/iudigitalradioapp/MainActivity.kt\ngit add app/src/main/java/com/example/iudigitalradioapp/ui/RadioScreen.kt\ngit add app/src/main/java/com/example/iudigitalradioapp/ui/RadioScreenDemo.kt\ngit add app/src/main/java/com/example/iudigitalradioapp/ui/components/StationSelector.kt\ngit add app/src/main/java/com/example/iudigitalradioapp/ui/components/PlaybackControls.kt\ngit add app/src/main/java/com/example/iudigitalradioapp/ui/components/PhotoPanel.kt\ngit add app/src/main/java/com/example/iudigitalradioapp/ui/theme/Color.kt\ngit add app/src/main/java/com/example/iudigitalradioapp/ui/theme/Theme.kt\ngit add app/src/main/java/com/example/iudigitalradioapp/ui/theme/Type.kt\ngit add app/src/androidTest/java/com/example/iudigitalradioapp/ui/RadioScreenTest.kt\n\ngit diff --cached\ngit commit -m \"Crea interfaz principal con Jetpack Compose\"")
add_note(doc, "Commit comprobado", "El esqueleto quedó registrado localmente como 08300b7. La rama aparece dos commits por delante del remoto porque contiene el commit de estado recibido desde main y el nuevo commit de interfaz.")

doc.add_heading("10 Copia ZIP opcional", level=1)
add_body(doc, "El ZIP sirve como respaldo del contenido registrado en HEAD. No reemplaza la rama ni el Pull Request.")
add_code(doc, "git archive --format=zip --output ..\\IU_Digital_Radio_Juan_Pablo_Gonzalez.zip HEAD")

doc.add_page_break()
doc.add_heading("11 Publicación de la rama", level=1)
add_body(doc, "Cuando la revisión local termine y main remoto ya contenga el módulo anterior aprobado, Juan Pablo publica únicamente feature/ui-compose.")
add_code(doc, "git switch feature/ui-compose\ngit status --short --branch\ngit push origin feature/ui-compose")
add_note(doc, "No usar push directo", "Juan Pablo no ejecuta git push origin main. El trabajo llega a main mediante un Pull Request revisado.")

doc.add_heading("12 Pull Request hacia main", level=1)
add_steps(doc, [
    "Abrir el repositorio en GitHub y seleccionar Compare and pull request.",
    "Confirmar base main y compare feature/ui-compose.",
    "Usar el título Crea interfaz principal con Jetpack Compose.",
    "Describir los componentes creados las pruebas y los límites del módulo.",
    "Solicitar la revisión de Juan Ardila.",
    "Fusionar sólo cuando el proyecto compile y la revisión esté aprobada.",
])
add_code(doc, "Resumen\n- Reemplaza la pantalla inicial por IU Digital Radio.\n- Agrega RadioScreen y componentes reutilizables.\n- Muestra las cinco emisoras en dos columnas sin desplazamiento horizontal.\n- Conecta temporalmente el estado mediante RadioScreenDemo.\n- Define colores tipografía y tema Material 3.\n- Agrega pruebas instrumentadas de contenido e interacción.\n\nVerificación\n- testDebugUnitTest assembleDebug\n- connectedDebugAndroidTest\n- 12 pruebas unitarias y 4 instrumentadas aprobadas.\n\nPendientes de integración\n- RadioRoute reemplazará RadioScreenDemo.\n- Cámara vibración y audio real serán conectados por sus responsables.")

doc.add_heading("13 Confirmación final en main", level=1)
add_body(doc, "Después de aprobar el Pull Request, el trabajo de Juan Pablo queda incorporado en main. Para comprobarlo localmente:")
add_code(doc, "git switch main\ngit pull --ff-only origin main\n.\\gradlew.bat testDebugUnitTest assembleDebug")
add_note(doc, "Fin del flujo", "Juan Pablo empieza desde main actualizado trabaja en feature/ui-compose publica esa rama y termina con su módulo integrado en main mediante revisión.")

doc.add_page_break()
doc.add_heading("14 Capturas recomendadas", level=1)
add_table(doc, ["Número", "Captura", "Qué demuestra"], [
    ("1", "main actualizado y cambio a feature/ui-compose", "La rama parte de una base aprobada."),
    ("2", "Árbol de paquetes ui components y ui theme", "La interfaz está organizada por responsabilidades."),
    ("3", "RadioScreen.kt en el editor", "La pantalla recibe estado y emite acciones."),
    ("4", "StationSelector con cinco emisoras", "La cuadrícula presenta dos columnas sin gesto horizontal."),
    ("5", "PhotoPanel.kt", "La UI está preparada para recibir una fotografía."),
    ("6", "Vista previa Compose", "La pantalla puede revisarse sin ejecutar efectos externos."),
    ("7", "Aplicación ejecutada en el emulador", "Las cinco emisoras aparecen sin desplazamiento horizontal."),
    ("8", "Botón en estado Pausar", "La interfaz responde a una acción y recompone."),
    ("9", "Pruebas instrumentadas aprobadas", "El contenido y la interacción fueron verificados."),
    ("10", "Commit 08300b7", "Los archivos de Juan Pablo quedaron registrados."),
    ("11", "Pull Request feature/ui-compose hacia main", "El cambio fue enviado a revisión."),
    ("12", "main después de la fusión", "El módulo terminó integrado."),
], widths=[Cm(1.8), Cm(6.0), Cm(7.8)], centered_columns={0})
add_body(doc, "Ejemplo de pie de figura: Figura 3. Creación de RadioScreen como función sin estado. Nota. Elaboración propia a partir del proyecto IU Digital Radio.")

doc.add_heading("15 Lista de cierre", level=1)
add_bullets(doc, [
    "[ ] Actualicé main antes de trabajar y confirmé feature/ui-compose como rama activa.",
    "[ ] Puedo explicar por qué RadioScreen recibe estado y onAction.",
    "[ ] Puedo distinguir ui components y ui.theme.",
    "[ ] Las cinco emisoras están visibles sin desplazamiento horizontal.",
    "[ ] La selección reproducción pausa y silencio cambian visualmente.",
    "[ ] El botón de cámara sólo emite RadioAction.OpenCamera.",
    "[ ] La aplicación y las pruebas finalizan con BUILD SUCCESSFUL.",
    "[ ] Excluí .idea output tmp y archivos personales del commit.",
    "[ ] Publiqué feature/ui-compose y abrí el Pull Request hacia main.",
    "[ ] Verifiqué main después de la fusión.",
])

doc.add_heading("16 Preguntas para explicar el trabajo", level=1)
add_bullets(doc, [
    "¿Qué diferencia existe entre RadioScreen y RadioScreenDemo?",
    "¿Por qué RadioScreen no usa remember para guardar su propio estado?",
    "¿Por qué RadioScreen usa LazyColumn y StationSelector usa Column y Row?",
    "¿Por qué los componentes emiten callbacks en lugar de reproducir audio directamente?",
    "¿Qué ocurre cuando RadioUiState cambia después de pulsar Reproducir?",
    "¿Por qué ui.theme es diferente del paquete ui aunque esté dentro de él?",
    "¿Qué diferencia existe entre push de la rama y fusión del Pull Request en main?",
])

doc.add_heading("17 Referencias técnicas", level=1)
add_body(doc, "Android Developers. (s. f.). Compose layout basics. https://developer.android.com/develop/ui/compose/layouts/basics")
add_body(doc, "Android Developers. (s. f.). State and Jetpack Compose. https://developer.android.com/develop/ui/compose/state")
add_body(doc, "Android Developers. (s. f.). Test your Compose layout. https://developer.android.com/develop/ui/compose/testing")
add_body(doc, "IU Digital. (s. f.). Evidencia de aprendizaje 3 Aplicación móvil Android IU Digital Radio Guía de orientación.")
add_body(doc, "Las referencias del informe final deben completarse con los datos bibliográficos disponibles en el aula y presentarse según APA séptima edición.")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
doc.save(OUTPUT)
print(OUTPUT)
