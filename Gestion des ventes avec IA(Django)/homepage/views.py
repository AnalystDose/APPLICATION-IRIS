from django.shortcuts import render
from django.views.generic import View, TemplateView
from inventory.models import Stock
from transactions.models import SaleBill, PurchaseBill, SaleItem
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.db.models.functions import ExtractYear


class HomeView(View):
    template_name = "home.html"

    def get(self, request):
        # Récupérer les données pour le graphique à barres (stocks)
        labels = []
        data = []
        stockqueryset = Stock.objects.filter(is_deleted=False).order_by('quantity')[:10]
        for item in stockqueryset:
            labels.append(item.name)
            data.append(item.quantity)

        # Récupérer les 3 meilleurs clients en fonction de la somme des montants dépensés
        top_clients = SaleBill.objects.values('name').annotate(
            total_spent=Coalesce(Sum('salebillno__totalprice'), 0)).order_by('-total_spent')[:5]

        # Créer des listes pour les noms des clients et les montants dépensés
        client_names = [client['name'] for client in top_clients]
        total_spent = [client['total_spent'] for client in top_clients]

        # Récupérer les données pour le graphique de ligne (évolution des ventes mensuelles)
        monthly_sales = SaleBill.objects.annotate(month=TruncMonth('time')).values('month').annotate(
            total_sales=Count('billno')).order_by('month')
        months = [entry['month'].strftime('%b %Y') for entry in monthly_sales]
        total_sales = [entry['total_sales'] for entry in monthly_sales]

        # Récupérer les données pour les 5 produits les plus vendus en termes de quantité
        top_products_quantity = SaleItem.objects.values('stock__name').annotate(
            total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]

        # Récupérer les données pour les 5 produits les plus vendus en termes de montant
        top_products_amount = SaleItem.objects.values('stock__name').annotate(total_amount=Sum('totalprice')).order_by(
            '-total_amount')[:5]

        # Créer des listes pour les noms des produits et les quantités/montants vendus
        top_products_quantity_names = [product['stock__name'] for product in top_products_quantity]
        top_products_quantity_values = [product['total_quantity'] for product in top_products_quantity]

        top_products_amount_names = [product['stock__name'] for product in top_products_amount]
        top_products_amount_values = [product['total_amount'] for product in top_products_amount]

        # Calculer le nombre total de ventes
        total_sales_count = SaleBill.objects.count()

        # Calculer le nombre total de clients distincts
        total_clients_count = SaleBill.objects.values('name').distinct().count()

        # Calculer le chiffre d'affaires total
        total_revenue = SaleBill.objects.aggregate(total_revenue=Sum('salebillno__totalprice'))['total_revenue']

        if not total_revenue:
            total_revenue = 0

            # Récupérer les données de vente par année
            yearly_sales = SaleBill.objects.annotate(year=ExtractYear('time')).values('year').annotate(
                total_sales=Sum('salebillno__totalprice')).order_by('year')

            # Préparation des données pour le graphique
            years = [entry['year'] for entry in yearly_sales]
            total_sales_by_year = [entry['total_sales'] for entry in yearly_sales]

        # Récupérer les données pour le chiffre d'affaires par année
        yearly_sales = SaleBill.objects.annotate(year=ExtractYear('time')).values('year').annotate(
            total_sales=Sum('salebillno__totalprice')).order_by('year')

        years = [entry['year'] for entry in yearly_sales]
        total_sales_by_year = [entry['total_sales'] for entry in yearly_sales]


        # Calculer le nombre total de produits
        total_products_count = Stock.objects.count()

        # Récupérer les 3 ventes les plus récentes
        sales = SaleBill.objects.order_by('-time')[:3]
        # Récupérer les 3 achats les plus récents
        purchases = PurchaseBill.objects.order_by('-time')[:3]
        # Contexte à passer au template
        context = {
            'labels': labels,
            'data': data,
            'client_names': client_names,
            'total_spent': total_spent,
            'monthly_sales': monthly_sales,
            'months': months,
            'total_sales': total_sales,
            'total_sales_count': total_sales_count,
            'total_clients_count': total_clients_count,
            'total_revenue': total_revenue,
            'total_products_count': total_products_count,
            'top_clients': top_clients,
            'sales': sales,
            'years': years,
            'total_sales_by_year': total_sales_by_year,
            'purchases': purchases,
            'top_products_quantity_names': top_products_quantity_names,
            'top_products_quantity_values': top_products_quantity_values,
            'top_products_amount_names': top_products_amount_names,
            'top_products_amount_values': top_products_amount_values,
        }
        return render(request, self.template_name, context)


class AboutView(TemplateView):
    template_name = "about.html"


class PredictionView(TemplateView):
    template_name = "prediction.html"
