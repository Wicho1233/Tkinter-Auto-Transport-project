from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os
from datetime import datetime
from data.db_autotranportesRepo import *

def generar_reporte_mal_estado_general(tr=None):
    """Genera un PDF con todos los mantenimientos en mal estado de todas las adaptaciones y divisiones"""
    datos_adaptacion = obtener_todos_mantenimientos_mal_estado_adaptacion()
    datos_division = obtener_todos_mantenimientos_mal_estado_division()
    
    if tr:
        datos_adaptacion = [d for d in datos_adaptacion if d[0] == tr]
        datos_division = [d for d in datos_division if d[0] == tr]
    
    if not datos_adaptacion and not datos_division:
        return False, "No hay mantenimientos con mal estado para generar el reporte"
    
    if not os.path.exists('reportes'):
        os.makedirs('reportes')
    
    filename = f"reportes/Reporte_Mal_Estado_Autotranportes_Cardenas_{tr if tr else 'General'}.pdf"
    
    try:
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []
        
        styles = getSampleStyleSheet()
        title_text = f"Reporte de Mantenimientos en Mal Estado - Autotransportes Cardenas" + (f" (TR: {tr})" if tr else "")
        title = Paragraph(title_text, styles['Title'])
        elements.append(title)
        
        elements.append(Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles['Normal']))
        elements.append(Paragraph(f"Total de registros: {len(datos_adaptacion) + len(datos_division)}", styles['Normal']))
        elements.append(Paragraph(" ", styles['Normal']))
        
        # Crear tabla con los datos de adaptación
        if datos_adaptacion:
            elements.append(Paragraph("Adaptaciones:", styles['Heading2']))
            headers = ["Tr", "Adaptación", "Mantenimiento", "Fecha", "KM Actual", "KM Mant.", "Costo"]
            table_data = [headers]
            
            for dato in datos_adaptacion:
                table_data.append([
                    str(dato[0]),  # Tr
                    dato[1],  # Adaptación
                    dato[2],  # Mantenimiento
                    dato[3],  # Fecha
                    str(dato[4]),  # KM Actual
                    str(dato[5]),  # KM Mantenimiento
                    f"${dato[6]:.2f}"  # Costo
                ])
            
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
            ]))
            
            elements.append(table)
            elements.append(Paragraph(" ", styles['Normal']))
        
        # Crear tabla con los datos de división
        if datos_division:
            elements.append(Paragraph("Divisiones:", styles['Heading2']))
            headers = ["Tr", "Número", "División", "Mantenimiento", "Fecha", "KM Actual", "KM Mant.", "Costo"]
            table_data = [headers]
            
            for dato in datos_division:
                table_data.append([
                    str(dato[0]),  # Tr
                    str(dato[1]),  # Número
                    dato[2],  # División
                    dato[3],  # Mantenimiento
                    dato[4],  # Fecha
                    str(dato[5]),  # KM Actual
                    str(dato[6]),  # KM Mantenimiento
                    f"${dato[7]:.2f}"  # Costo
                ])
            
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
            ]))
            
            elements.append(table)
        
        doc.build(elements)
        return True, filename
        
    except Exception as e:
        return False, str(e)