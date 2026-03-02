try:
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False
import tkinter.messagebox as messagebox

def export_pdf(metrics_data, filename="OS_Simulation_Report.pdf"):
    if not HAS_REPORTLAB:
        messagebox.showerror("Export Failed", "reportlab module is not installed. Please run: pip install reportlab")
        return False
        
    doc = SimpleDocTemplate(filename)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("OS Disk Scheduling & Performance Report", styles['Title']))
    elements.append(Spacer(1, 12))

    for key, value in metrics_data.items():
        elements.append(Paragraph(f"<b>{key}:</b> {value}", styles['Normal']))
        elements.append(Spacer(1, 6))

    try:
        doc.build(elements)
        messagebox.showinfo("Export Success", f"Report successfully saved as {filename}")
        return True
    except Exception as e:
        messagebox.showerror("Export Failed", str(e))
        return False
