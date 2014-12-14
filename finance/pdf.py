from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from django.templatetags.static import static

from core.models import *

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm, cm, inch
from reportlab.platypus import Table, TableStyle , Paragraph, Frame, Spacer ,SimpleDocTemplate, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import BaseDocTemplate,  PageTemplate , KeepTogether
from reportlab.platypus import PageBreak 
from datetime import datetime

import datetime

GLOBAL_EMPTY_MSG = "N/A"

styles = getSampleStyleSheet()
styleN = styles['Normal']
styleH = styles['Heading1']

base_url = "core/static/core/"
MAX_IMG_SIZE = 300

def date_cleaner (object):
	"""Prevents object-not-found errors and replaces *None* with GLOBAL_EMPTY_MSG. """
	if object and hasattr(object, 'date'):
		return object.date()
	elif object:
		return object
	else:
		return GLOBAL_EMPTY_MSG

def node_cleaner(object):
	"""Prevents object-not-found errors and replaces *None* with GLOBAL_EMPTY_MSG. """
	if object:
		return str(object)
	else:
		return GLOBAL_EMPTY_MSG

def bank_depo_pdf(request, latest_node_list):
	"""
	Takes data from Node and fills out a .PDF 

	"""

	doc_name = "Bank_Deposit"
	doc_name += datetime.datetime.now().strftime("_%m_%d_%Y")

	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename='+doc_name.replace(" ","%20")

	url = base_url + "images/Icon_new.png"

	url = base_url + "images/far_history.png"
	far_history = Image(url,507,114)

	styles = getSampleStyleSheet()

	far_main_data = [[Paragraph('<b>ID</b>',styles['Normal']),Paragraph('<b>Date</b>',styles['Normal']),Paragraph('<b>Bank</b>',styles['Normal']),
						Paragraph('<b>Depositor</b>',styles['Normal']),Paragraph('<b>Amount</b>',styles['Normal'])]]

	far_detail_data = []

	if latest_node_list:
		for node in latest_node_list:
			date = node.date_created [:10]
			for child in node.node_set.all():
				if child.name == "bank name":
					bank = child
				elif child.name == "depositor":
					depositor = child
				elif child.name == "amount":
					amount = child

			far_main_data += [[node_cleaner(node.id),date,node_cleaner(bank.desc),node_cleaner(depositor.desc),
								node_cleaner(amount.desc)]]

			far_detail_data += [[" "," "],
								[Paragraph('<b>ID:</b>',styles['Normal']),node_cleaner(node.id)],
								[Paragraph('<b>Date:</b>',styles['Normal']),date],
								[Paragraph('<b>Bank:</b>',styles['Normal']),node_cleaner(bank.desc)],
								[Paragraph('<b>Depositor:</b>',styles['Normal']),node_cleaner(depositor.desc)],
								[Paragraph('<b>Amount:</b>',styles['Normal']),node_cleaner(amount.desc)],
								[Paragraph('<b>Description:</b>',styles['Normal']),node_cleaner(node.desc)]]


	far_main_table = Table(far_main_data, colWidths = 1.2*inch)
	far_detail_table = Table(far_detail_data,  hAlign='LEFT', colWidths = 1.2*inch)

	far_main_table.setStyle(TableStyle([
 										('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
 										('BOX', (0,0), (-1,-1), 0.25, colors.black),
        								('LINEBELOW', (0,0), (-1,0), 1, colors.black),
        								('BACKGROUND', (0,0), (-1,0), colors.HexColor('#C0C0C0')),
        								('ROWBACKGROUNDS', (0,1), (-1, -1), [colors.white, colors.HexColor('#E0E0E0')])
 										]))

	side_margin = 45
	doc = SimpleDocTemplate(response,
								rightMargin=side_margin,
								leftMargin=side_margin,
								topMargin=inch,
								bottomMargin=inch)

	"""Story = [Spacer(0,0)]

	Story.append(far_history)
	Story.append(Spacer(0,15))
	Story.append(far_main_table)
	Story.append(Spacer(0,20))"""

	Story = []

	styleH = styles['Heading1']

	#add some flowables
	Story.append(Paragraph("Bank Deposit History",styleH))
	Story.append(Spacer(0,15))
	Story.append(far_main_table)

	Story.append(PageBreak())

	Story.append(Paragraph("Bank Deposit Details",styleH))
	Story.append(Spacer(0,15))
	Story.append(far_detail_table)

	doc.build(Story)

	return response	

def expend_pdf(request, latest_node_list):
	"""
	Takes data from Node and fills out a .PDF 

	"""

	doc_name = "Expenditure"
	doc_name += datetime.datetime.now().strftime("_%m_%d_%Y")

	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename='+doc_name.replace(" ","%20")

	styles = getSampleStyleSheet()

	far_main_data = [[Paragraph('<b>ID</b>',styles['Normal']),Paragraph('<b>Date</b>',styles['Normal']),Paragraph('<b>Bank</b>',styles['Normal']),
						Paragraph('<b>Payment To</b>',styles['Normal']),Paragraph('<b>Amount</b>',styles['Normal'])]]

	far_detail_data = []

	if latest_node_list:
		for node in latest_node_list:
			date = str(node.date_created)
			date = date [:10]
			for child in node.node_set.all():
				if child.name == "payto":
					payto = child
				elif child.name == "amount":
					amount = child

			far_main_data += [[node_cleaner(node.id),date,node_cleaner(payto.desc),
										node_cleaner(amount.desc)]]

			far_detail_data += [[" "," "],
								[Paragraph('<b>ID:</b>',styles['Normal']),node_cleaner(node.id)],
								[Paragraph('<b>Date:</b>',styles['Normal']),date],
								[Paragraph('<b>Payment To:</b>',styles['Normal']),node_cleaner(payto.desc)],
								[Paragraph('<b>Amount:</b>',styles['Normal']),node_cleaner(amount.desc)],
								[Paragraph('<b>Description:</b>',styles['Normal']),node_cleaner(node.desc)]]


	far_main_table = Table(far_main_data, colWidths = 1.2*inch)
	far_detail_table = Table(far_detail_data,  hAlign='LEFT', colWidths = 1.2*inch)

	far_main_table.setStyle(TableStyle([
 										('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
 										('BOX', (0,0), (-1,-1), 0.25, colors.black),
        								('LINEBELOW', (0,0), (-1,0), 1, colors.black),
        								('BACKGROUND', (0,0), (-1,0), colors.HexColor('#C0C0C0')),
        								('ROWBACKGROUNDS', (0,1), (-1, -1), [colors.white, colors.HexColor('#E0E0E0')])
 										]))

	side_margin = 45
	doc = SimpleDocTemplate(response,
								rightMargin=side_margin,
								leftMargin=side_margin,
								topMargin=inch,
								bottomMargin=inch)

	"""Story = [Spacer(0,0)]

	Story.append(far_history)
	Story.append(Spacer(0,15))
	Story.append(far_main_table)
	Story.append(Spacer(0,20))"""

	Story = []

	styleH = styles['Heading1']

	#add some flowables
	Story.append(Paragraph("Expenditure History",styleH))
	Story.append(Spacer(0,15))
	Story.append(far_main_table)

	Story.append(PageBreak())

	Story.append(Paragraph("Expenditure Details",styleH))
	Story.append(Spacer(0,15))
	Story.append(far_detail_table)

	doc.build(Story)

	return response	

def pay_rec_pdf(request, latest_node_list):
	"""
	Takes data from Node and fills out a .PDF 

	"""

	doc_name = "Payment_Received"
	doc_name += datetime.datetime.now().strftime("_%m_%d_%Y")


	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename='+doc_name.replace(" ","%20")

	styles = getSampleStyleSheet()

	far_main_data = [[Paragraph('<b>ID</b>',styles['Normal']),Paragraph('<b>Date</b>',styles['Normal']),Paragraph('<b>Bank</b>',styles['Normal']),
						Paragraph('<b>Payment From</b>',styles['Normal']),Paragraph('<b>Amount</b>',styles['Normal'])]]

	far_detail_data = []

	if latest_node_list:
		for node in latest_node_list:
			date = node.date_created [:10]
			for child in node.node_set.all():
				if child.name == "payfrom":
					payto = child
				elif child.name == "amount":
					amount = child
			
			far_main_data += [[node_cleaner(node.id),date,node_cleaner(payfrom.desc),
										node_cleaner(amount.desc)]]

			far_detail_data += [[" "," "],
								[Paragraph('<b>ID:</b>',styles['Normal']),node_cleaner(node.id)],
								[Paragraph('<b>Date:</b>',styles['Normal']),date],
								[Paragraph('<b>Payment From:</b>',styles['Normal']),node_cleaner(payfrom.desc)],
								[Paragraph('<b>Amount:</b>',styles['Normal']),node_cleaner(amount.desc)],
								[Paragraph('<b>Description:</b>',styles['Normal']),node_cleaner(node.desc)]]


	far_main_table = Table(far_main_data, colWidths = 1.2*inch)
	far_detail_table = Table(far_detail_data,  hAlign='LEFT', colWidths = 1.2*inch)

	far_main_table.setStyle(TableStyle([
 										('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
 										('BOX', (0,0), (-1,-1), 0.25, colors.black),
        								('LINEBELOW', (0,0), (-1,0), 1, colors.black),
        								('BACKGROUND', (0,0), (-1,0), colors.HexColor('#C0C0C0')),
        								('ROWBACKGROUNDS', (0,1), (-1, -1), [colors.white, colors.HexColor('#E0E0E0')])
 										]))

	side_margin = 45
	doc = SimpleDocTemplate(response,
								rightMargin=side_margin,
								leftMargin=side_margin,
								topMargin=inch,
								bottomMargin=inch)

	"""Story = [Spacer(0,0)]

	Story.append(far_history)
	Story.append(Spacer(0,15))
	Story.append(far_main_table)
	Story.append(Spacer(0,20))"""

	Story = []

	styleH = styles['Heading1']

	#add some flowables
	Story.append(Paragraph("Payment Received History",styleH))
	Story.append(Spacer(0,15))
	Story.append(far_main_table)

	Story.append(PageBreak())

	Story.append(Paragraph("Payment Received Details",styleH))
	Story.append(Spacer(0,15))
	Story.append(far_detail_table)

	doc.build(Story)

	return response	