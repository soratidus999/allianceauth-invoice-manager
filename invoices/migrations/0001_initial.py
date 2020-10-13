# Generated by Django 3.1.1 on 2020-10-08 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('corptools', '0035_auto_20200929_0114'),
        ('eveonline', '0012_index_additions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=None, max_digits=20, null=True)),
                ('invoice_ref', models.CharField(max_length=72)),
                ('due_date', models.DateTimeField()),
                ('notified', models.DateTimeField()),
                ('paid', models.BooleanField()),
                ('character', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoices', to='eveonline.evecharacter')),
                ('payment', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoice', to='corptools.corporationwalletjournalentry')),
            ],
        ),
    ]