##############################################################################################################################
#
#  PROGRAMA CREADO POR M8AX - MARCOS OCHOA DIEZ, PARA PINTAR PÍXELES DE DIFERENTES COLORES, SI COINCIDEN CON NÚMEROS PRIMOS...
#  SE PUEDE APLICAR A IMAGENES O FOTOS, PARA DARLES UN TOQUE ESPECIAL... UN TOQUE FRIKI xD...
#  Ejemplo - py m8ax_img_primos.py -ip "1-100,25,75-jpg-0"
#  Ayuda - py m8ax_img_primos.py --help
#
##############################################################################################################################

from PIL.PngImagePlugin import PngInfo
from PIL import Image, ImageChops, ImageEnhance, ImageOps
import time
import math
import errno
import sympy
import numpy as np
import glob
import os
import cv2
import sys
import click

@click.command()
@click.option(
    "-ip",
    "--impr",
    required=False,
    type=str,
    default="",
    help="Formato -ip 'Num_Comienzo-RGB_Color-TipoImagen-Num'. Ejemplo: -ip '1-15,120,75-png-3'. Sirve Para Pintar Píxeles Primos En Imágenes, Los Píxeles De La Imágen Comenzarán Por El Número Que Pases Con La Opción -ip. Es Decir, Si Le Damos El Número 997, Que Sabemos Que Es Un Número Primo, El Pixel Número 1 De La Imágen Estará Pintado, El Siguiente No, Porque Sería El 998 Y 998 No Es Primo... El Color RGB, Cada Color Separado Por Una , TipoImagen png, jpg, bmp, Etc... Y El Último Número... Si Es 0, Número De Comienzo, El Especificado Y El Color También. Si Ponemos 1, El Número Será El Especificado Y El Color Aleatorio, Pero Todos Iguales En Color. Si 2, Número Aleatorio Y Colores Aleatorios, Cada Pixel Primo De Un Color. Si 3, Número Aleatorio Y Colores También. Si 4, Número Aleatorio, Pero Respeta El Color Que Hemos Puesto Nosotros. Si 5, Número Aleatorio Y Color Aleatorio, Pero Todos El Mismo Color En Cada "
    + "Imágen. Si 6, Número Especificado Y Color También, Pero Nos Añadirá También, En Color Amarillo, Los Píxeles Que Correspondan A Números Primos Gemelos, Obviamente... Empezando Desde El Número Que Nosotros Le Hemos Indicado... Así Que Habrá Que Elegir Un Color Diferente Al Amarillo, Para Poder Distinguirlos Correctamente.",
)

def run(impr: str):

    impr = "" if impr is None else impr

    if impr == "":
        print(
            "\nPor Lo Visto... Has Seleccionado Que En La Imágen, Se Pinten Píxeles Primos, Pero Lo Has Especificado Mal, Debes Especificar Así...\nEjemplo: -ip 5-24,56,100-png-2 Estamos Indicando Que Empiece El Pixel 1 De La Imágen Como Si Fuera El Número 5 Y Se Pintarán Todos Los Píxeles Primos\nA Partir Del Número 5, Con El Color RGB 24,56,100. png - Solo Se Convertirán Las Imágenes png Y El Último 2 Indica Que Obviemos Lo Anterior Y Que Tanto Los Colores\nDe Los Píxeles Como El Número De Comienzo Del Pixel 1 En Cada Imágen, Sea Aleatorio. Así Que... Si Queremos Que Se Cumpla Lo Que Nosotros Queremos, El 2 Del Final, Debe Ser 0.\nOtro Ejemplo: -ip 1000000000-255,0,0-png-0 El Pixel 1 De La Imágen Sera El Número 1000000000, El Segundo... 1000000001 Y Se Pintarán Los\nQue Sean Primos Y Como Hemos Puesto Al Final Un 0, Pues Se Cumplirá Lo Que Hemos Dicho, Si Fuera Un 2, El Número De Comienzo\nSerá Aleatorio En Cada Imágen Generada Y Los Colores De Los Pixeles También.\n\n- NOTA"
            + " IMPORTANTE -"
        )
        print(
            "\nEl Número Del Final, Solo Puede Tener Siete Valores, O 0, O 1, O 2, O 3, O 4, O 5, O 6... Los Voy A Explicar Ahora Con Más Detalle, Para Que Se Entiendan..."
        )
        print(
            "\nSi Al Final Ponemos Un 0 - El Número De Comienzo, Será El Especificado Y El Color De Los Píxeles Primos Pintados Será El Especificado Por Tí."
        )
        print(
            "\nSi Al Final Ponemos Un 1 - El Número De Comienzo, Será El Especificado, Pero El Color De Los Píxeles, En Cada Imágen Generada Cambiará, Pero Serán Todos Iguales, Del Mismo Color."
        )
        print(
            "\nSi Al Final Ponemos Un 2 - El Número De Comienzo, Será Aleatorio Y El Color De Cada Pixel Pintado, También, Así En Todas Las Imágenes Generadas."
        )
        print(
            "\nSi Al Final Ponemos Un 3 - El Número De Comienzo, Será El Especificado, Pero El Color De Cada Pixel Pintado Será Aleatorio, Así En Cada Imágen Generada."
        )
        print(
            "\nSi Al Final Ponemos Un 4 - El Número De Comienzo, Será Aleatorio, Pero Se Respeta El Color Que Hemos Elegido, Así... Para Todas Las Imágenes Generadas."
        )
        print(
            "\nSi Al Final Ponemos Un 5 - El Número De Comienzo, Será Aleatorio Y El Color De Cada Pixel En Cada Imágen Generada Cambiará, Pero En Cada Imágen Generada, Todos Serán Del Mismo Color."
        )
        print(
            "\nSi Al Final Ponemos Un 6 - El Número De Comienzo, Será El Especificado Y El Color También, Pero Además... Se Pintarán De Color Amarillo, Los Píxeles Que Coincidan Con Números Primos Gemelos.\n\nSe Pintarán De Amarillo, Así Que Procura Elegir Otro Color, Para Pintar Los Píxeles Primos Y Se Vea La Diferencia..."
        )
        print(
            "\nEn La Primera Ejecución Se Crearán Las Carpetas M8AX-Ilustraciones-Si_Primos Y M8AX-Ilustraciones-No_Primos, En Esta Última Meteremos Las Imágenes A Pintar Píxeles Primos Y En La Siguiente Ejecución, Se Realizará El Pintado."
        )
        print("\n\n... Espero Que Todo Este Aclarado Y Comprendido ...\n")

        try:
            os.mkdir("M8AX-Ilustraciones-Si_Primos")
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        try:
            os.mkdir("M8AX-Ilustraciones-No_Primos")
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        sys.exit(1)

    if impr != "":
        try:
            impri, colorcete, tipofi, colaleynum = impr.split(sep="-")
            impri = int(impri)
            colorc1, colorc2, colorc3 = colorcete.split(sep=",")
            colorc1 = int(colorc1)
            colorc2 = int(colorc2)
            colorc3 = int(colorc3)
            colorcete = [colorc3, colorc2, colorc1]
            colaleynum = int(colaleynum)

            try:
                os.mkdir("M8AX-Ilustraciones-Si_Primos")
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            try:
                os.mkdir("M8AX-Ilustraciones-No_Primos")
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
        except:
            print(
                "\nPor Lo Visto... Has Seleccionado Que En La Imágen, Se Pinten Píxeles Primos, Pero Lo Has Especificado Mal, Debes Especificar Así...\nEjemplo: -ip 5-24,56,100-png-2 Estamos Indicando Que Empiece El Pixel 1 De La Imágen Como Si Fuera El Número 5 Y Se Pintarán Todos Los Píxeles Primos\nA Partir Del Número 5, Con El Color RGB 24,56,100. png - Solo Se Convertirán Las Imágenes png Y El Último 2 Indica Que Obviemos Lo Anterior Y Que Tanto Los Colores\nDe Los Píxeles Como El Número De Comienzo Del Pixel 1 En Cada Imágen, Sea Aleatorio. Así Que... Si Queremos Que Se Cumpla Lo Que Nosotros Queremos, El 2 Del Final, Debe Ser 0.\nOtro Ejemplo: -ip 1000000000-255,0,0-png-0 El Pixel 1 De La Imágen Sera El Número 1000000000, El Segundo... 1000000001 Y Se Pintarán Los\nQue Sean Primos Y Como Hemos Puesto Al Final Un 0, Pues Se Cumplirá Lo Que Hemos Dicho, Si Fuera Un 2, El Número De Comienzo\nSerá Aleatorio En Cada Imágen Generada Y Los Colores De Los Pixeles También.\n\n- NOTA"
                + " IMPORTANTE -"
            )
            print(
                "\nEl Número Del Final, Solo Puede Tener Siete Valores, O 0, O 1, O 2, O 3, O 4, O 5, O 6... Los Voy A Explicar Ahora Con Más Detalle, Para Que Se Entiendan..."
            )
            print(
                "\nSi Al Final Ponemos Un 0 - El Número De Comienzo, Será El Especificado Y El Color De Los Píxeles Primos Pintados Será El Especificado Por Tí."
            )
            print(
                "\nSi Al Final Ponemos Un 1 - El Número De Comienzo, Será El Especificado, Pero El Color De Los Píxeles, En Cada Imágen Generada Cambiará, Pero Serán Todos Iguales, Del Mismo Color."
            )
            print(
                "\nSi Al Final Ponemos Un 2 - El Número De Comienzo, Será Aleatorio Y El Color De Cada Pixel Pintado, También, Así En Todas Las Imágenes Generadas."
            )
            print(
                "\nSi Al Final Ponemos Un 3 - El Número De Comienzo, Será El Especificado, Pero El Color De Cada Pixel Pintado Será Aleatorio, Así En Cada Imágen Generada."
            )
            print(
                "\nSi Al Final Ponemos Un 4 - El Número De Comienzo, Será Aleatorio, Pero Se Respeta El Color Que Hemos Elegido, Así... Para Todas Las Imágenes Generadas."
            )
            print(
                "\nSi Al Final Ponemos Un 5 - El Número De Comienzo, Será Aleatorio Y El Color De Cada Pixel En Cada Imágen Generada Cambiará, Pero En Cada Imágen Generada, Todos Serán Del Mismo Color."
            )
            print(
                "\nSi Al Final Ponemos Un 6 - El Número De Comienzo, Será El Especificado Y El Color También, Pero Además... Se Pintarán De Color Amarillo, Los Píxeles Que Coincidan Con Números Primos Gemelos.\n\nSe Pintarán De Amarillo, Así Que Procura Elegir Otro Color, Para Pintar Los Píxeles Primos Y Se Vea La Diferencia..."
            )
            print(
                "\nEn La Primera Ejecución Se Crearán Las Carpetas M8AX-Ilustraciones-Si_Primos Y M8AX-Ilustraciones-No_Primos, En Esta Última Meteremos Las Imágenes A Pintar Píxeles Primos Y En La Siguiente Ejecución, Se Realizará El Pintado."
            )
            print("\n\n... Espero Que Todo Este Aclarado Y Comprendido ...\n")

            try:
                os.mkdir("M8AX-Ilustraciones-Si_Primos")
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            try:
                os.mkdir("M8AX-Ilustraciones-No_Primos")
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            sys.exit(1)

    numimg = 0

    os.chdir("M8AX-Ilustraciones-No_Primos")

    if impr != "":
        traa = time.time()
        cuantospng = len(glob.glob("*." + tipofi))

        for filename in sorted(glob.glob("*." + tipofi), key=os.path.getmtime):
            numimg = numimg + 1
            comienzodesden = 0
            elultimop = 0
            auxcomienzo = 0
            cuantosprimos = 0
            antfil = 0
            antcol = 0
            primgeme = 0
            antprim = 0
            imagenprima = cv2.imread(filename)
            wip = imagenprima.shape[1]
            hep = imagenprima.shape[0]

            if hep > wip:
                cambiando = wip
                wip = hep
                hep = cambiando
            else:
                cambiando = hep
                hep = wip
                wip = cambiando

            if colaleynum == 1 or colaleynum == 5:
                colorcete = [
                    np.random.randint(0, 256),
                    np.random.randint(0, 256),
                    np.random.randint(0, 256),
                ]

            if colaleynum == 2 or colaleynum == 4 or colaleynum == 5:
                impri = np.random.randint(
                    2147483647, 9223372036854775807, dtype=np.int64
                )

            comienzodesden = impri
            auxcomienzo = comienzodesden
            cuantosprimos = 0
            comipri = time.time()
            print(
                f"\n... Pintando Píxeles Primos, En La Imágen - {numimg} De {cuantospng} ...\n"
            )
            tiembarra = time.time()

            for fila in range(wip):
                for columna in range(hep):
                    if sympy.isprime(comienzodesden):
                        if colaleynum == 2 or colaleynum == 3:
                            colorcete = [
                                np.random.randint(0, 256),
                                np.random.randint(0, 256),
                                np.random.randint(0, 256),
                            ]
                        cuantosprimos = cuantosprimos + 1
                        elultimop = comienzodesden
                        imagenprima[fila, columna] = colorcete
                        if colaleynum == 6 and antprim > 2:
                            if comienzodesden - antprim == 2:
                                primgeme = primgeme + 1
                                imagenprima[antfil, antcol] = [0, 255, 0]
                                imagenprima[fila, columna] = [0, 255, 0]
                        antfil = fila
                        antcol = columna
                        antprim = comienzodesden
                    comienzodesden = comienzodesden + 1
                barra_progreso_vibrante(
                    (fila * columna * 100) / (wip * hep), 100, tiembarra
                )

            barra_progreso_vibrante((wip * hep * 100) / (wip * hep), 100, tiembarra)
            print(
                "\n\n... Trabajo De Pintado De Píxeles Primos, Terminado Correctamente ..."
            )

            finpri = time.time()
            pcentajep = (cuantosprimos * 100) / (comienzodesden - auxcomienzo)
            pcentajeg = ((2 * primgeme) * 100) / (comienzodesden - auxcomienzo)

            cv2.imwrite(
                "../M8AX-Ilustraciones-Si_Primos/"
                + str(numimg)
                + "-ImG_Pixel_Primos-"
                + filename,
                imagenprima,
            )

            targetImage = Image.open(
                "../M8AX-Ilustraciones-Si_Primos/"
                + str(numimg)
                + "-ImG_Pixel_Primos-"
                + filename
            )

            metadata = PngInfo()

            metadata.add_text(
               "MvIiIaX.M8AX - Comentario - ",
                "... Por Muchas Vueltas Que Demos, Siempre Tendremos El Culo Atrás ..."
                + "\n\nImágen Con "
                + str(comienzodesden-auxcomienzo)
                + " De Píxeles, De Los Cuáles, Hemos Coloreado, "
                + str(cuantosprimos)
                + ", Un "
                + str(round(pcentajep, 3))
                + "% De La Imágen.\n\nEmpezando Desde El Pixel Número 1 De La Imágen, Como Si Fuera El Número "
                + str(auxcomienzo)
                + ".\n\nEl Último Número Primo Pintado, Es El "
                + str(elultimop)
                + ".\n\nVelocidad De Píxeles Primos Pintados - "
                + str(round(cuantosprimos / (finpri - comipri), 2))
                + " PPP/Seg.",
            )

            metadata.add_text("M8AX-ID", str(10031977))

            try:
                targetImage.save(
                "../M8AX-Ilustraciones-Si_Primos/"
                + str(numimg)
                + "-ImG_Pixel_Primos-"
                + filename,
                  pnginfo=metadata,
                )

            except:
                print("\nNo Se Han Podido Grabar Los Metadatos En La Imágen, Con Los Datos Del Proceso De Cálculo. Imágen Demasiado Grande... Aún Así, La Imágen Está Correcta.")

            cv2.imshow("--- M8AX IMAGEN PRIMA ---", imagenprima)

            if cuantospng == 1:
                cv2.waitKey(0)
            else:
                cv2.waitKey(1)

            if colaleynum == 0:
                print(
                    f"\nImágen Con {comienzodesden-auxcomienzo} De Píxeles, De Los Cuáles, Hemos Coloreado, {cuantosprimos}, Con El Color RGB - R-{colorc1} G-{colorc2} B-{colorc3} - "
                    + coloreando(colorc1, colorc2, colorc3, "█████")
                    + f", Un {round(pcentajep,3)}% De La Imágen.\n\nEmpezando Desde El Pixel Número 1 De La Imágen, Como Si Fuera El Número {auxcomienzo}.\n\nEl Último Número Primo Pintado, Es El {elultimop}.\n\nVelocidad De Píxeles Primos Pintados - {round(cuantosprimos/(finpri-comipri),2)} PPP/Seg."
                )

            if colaleynum == 1:
                print(
                    f"\nImágen Con {comienzodesden-auxcomienzo} De Píxeles, De Los Cuáles, Hemos Coloreado, {cuantosprimos}, Con El Color RGB - R-{colorcete[2]} G-{colorcete[1]} B-{colorcete[0]} - "
                    + coloreando(colorcete[2], colorcete[1], colorcete[0], "█████")
                    + f", Un {round(pcentajep,3)}% De La Imágen.\n\nEmpezando Desde El Pixel Número 1 De La Imágen, Como Si Fuera El Número {auxcomienzo}.\n\nEl Último Número Primo Pintado, Es El {elultimop}.\n\nVelocidad De Píxeles Primos Pintados - {round(cuantosprimos/(finpri-comipri),2)} PPP/Seg."
                )

            if colaleynum == 2:
                print(
                    f"\nImágen Con {comienzodesden-auxcomienzo} De Píxeles, De Los Cuáles, Hemos Coloreado, {cuantosprimos}, Con Colores Aleatorios, Un {round(pcentajep,3)}% De La Imágen.\n\nEmpezando Desde El Pixel Número 1 De La Imágen, Como Si Fuera El Número {auxcomienzo}.\n\nEl Último Número Primo Pintado, Es El {elultimop}.\n\nVelocidad De Píxeles Primos Pintados - {round(cuantosprimos/(finpri-comipri),2)} PPP/Seg."
                )

            if colaleynum == 3:
                print(
                    f"\nImágen Con {comienzodesden-auxcomienzo} De Píxeles, De Los Cuáles, Hemos Coloreado, {cuantosprimos}, Con Colores Aleatorios, Un {round(pcentajep,3)}% De La Imágen.\n\nEmpezando Desde El Pixel Número 1 De La Imágen, Como Si Fuera El Número {auxcomienzo}.\n\nEl Último Número Primo Pintado, Es El {elultimop}.\n\nVelocidad De Píxeles Primos Pintados - {round(cuantosprimos/(finpri-comipri),2)} PPP/Seg."
                )

            if colaleynum == 4:
                print(
                    f"\nImágen Con {comienzodesden-auxcomienzo} De Píxeles, De Los Cuáles, Hemos Coloreado, {cuantosprimos}, Con El Color RGB - R-{colorc1} G-{colorc2} B-{colorc3} - "
                    + coloreando(colorc1, colorc2, colorc3, "█████")
                    + f", Un {round(pcentajep,3)}% De La Imágen.\n\nEmpezando Desde El Pixel Número 1 De La Imágen, Como Si Fuera El Número {auxcomienzo}.\n\nEl Último Número Primo Pintado, Es El {elultimop}.\n\nVelocidad De Píxeles Primos Pintados - {round(cuantosprimos/(finpri-comipri),2)} PPP/Seg."
                )

            if colaleynum == 5:
                print(
                    f"\nImágen Con {comienzodesden-auxcomienzo} De Píxeles, De Los Cuáles, Hemos Coloreado, {cuantosprimos}, Con El Color RGB - R-{colorcete[2]} G-{colorcete[1]} B-{colorcete[0]} - "
                    + coloreando(colorcete[2], colorcete[1], colorcete[0], "█████")
                    + f", Un {round(pcentajep,3)}% De La Imágen.\n\nEmpezando Desde El Pixel Número 1 De La Imágen, Como Si Fuera El Número {auxcomienzo}.\n\nEl Último Número Primo Pintado, Es El {elultimop}.\n\nVelocidad De Píxeles Primos Pintados - {round(cuantosprimos/(finpri-comipri),2)} PPP/Seg."
                )

            if colaleynum == 6:
                print(
                    f"\nImágen Con {comienzodesden-auxcomienzo} De Píxeles, De Los Cuáles, Hemos Coloreado, {cuantosprimos}, Con El Color RGB - R-{colorc1} G-{colorc2} B-{colorc3} - "
                    + coloreando(colorc1, colorc2, colorc3, "█████")
                    + f", Un {round(pcentajep,3)}% De La Imágen.\n\nEmpezando Desde El Pixel Número 1 De La Imágen, Como Si Fuera El Número {auxcomienzo}.\n\nEl Último Número Primo Pintado, Es El {elultimop}. Además, Hemos Pintado {primgeme*2} Números Primos Gemelos De Color Amarillo, {primgeme} Parejas, Un {round(pcentajeg,3)}% De La Imágen.\n\nVelocidad De Píxeles Primos Pintados - {round(cuantosprimos/(finpri-comipri),2)} PPP/Seg.\n\nVelocidad De Píxeles Primos Gemelos Pintados - {round((primgeme*2)/(finpri-comipri),2)} PPGP/Seg."
                )

    cv2.destroyAllWindows()
    trab = time.time()
    print(
        f"\nFin Del Pintado De Pixeles Primos... Tiempo Total De Trabajo - {round((trab-traa),3)} Segundos. A Una Media De {round(cuantospng/(trab-traa),3)} Img/Seg Procesadas... {round(60*(cuantospng/(trab-traa)),3)} Img/Min. {round(3600*(cuantospng/(trab-traa)),3)} Img/Hor.\n\nBy M8AX..."
    )

def coloreando(r, g, b, text):
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

def segahms(segundos):
    horas = int(segundos / 60 / 60)
    segundos -= horas * 60 * 60
    minutos = int(segundos / 60)
    segundos -= minutos * 60
    return f"{horas}h:{minutos}m:{int(segundos)}s"

def barra_progreso_vibrante(progreso, total, tiembarra):
    porcen = 100 * (progreso / float(total))
    segrestante = 0
    if porcen > 0:
        segrestante = (100 * (tiembarra - time.time()) / porcen) - (
            tiembarra - time.time()
        )
    barra = "█" * int(porcen) + "-" * (100 - int(porcen))
    print(
        f"\r\033[38;2;{np.random.randint(0, 256)};{np.random.randint(0, 256)};{np.random.randint(0, 256)}m|{barra}| - ETA - {segahms(segrestante*-1)} - {porcen:.2f}%",
        end="\r\033[0m",
    )

if __name__ == "__main__":
    run()
