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

def build_pdf(request, latest_node_list):
	"""
	Takes data from Node and fills out a .PDF 

	"""

	doc_name = "Bank_Deposit"
	doc_name += datetime.datetime.now().strftime("_%m_%d_%Y_%I_%M%p")

	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename='+doc_name.replace(" ","%20")

	url = base_url + "images/Icon_new.png"

	url = base_url + "images/far_history.png"
	far_history = Image(url,507,114)

	styles = getSampleStyleSheet()

	far_main_data = [["ID","Bank","Depositor","Amount","Description"]]

	far_detail_data = ["",""]

	if latest_node_list:
		for node in latest_node_list:
			for child in node.node_set.all():
				if child.name == "bank name":
					bank = child
				elif child.name == "depositor":
					depositor = child
				elif child.name == "amount":
					amount = child
			far_main_data += [[node_cleaner(node.id),node_cleaner(bank.desc),node_cleaner(depositor.desc),
								node_cleaner(amount.desc),node_cleaner(node.desc)]]
			far_detail_data += [[" "," "],
								["ID:",node_cleaner(node.id)],
								["Bank:",node_cleaner(bank.desc)],
								["Depositor:",node_cleaner(depositor.desc)],
								["Amount:",node_cleaner(amount.desc)],
								["Description:",node_cleaner(node.desc)]]


	far_main_table = Table(far_main_data)
	far_detail_table = Table(far_detail_data)

	far_main_table.setStyle(TableStyle([
 										('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
 										('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
 										('BOX', (0,0), (-1,-1), 0.25, colors.black),
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
	Story.append(Paragraph("Bank Deposits",styleH))
	Story.append(far_main_table)
	Story.append(far_detail_table)

	doc.build(Story)

	return response	