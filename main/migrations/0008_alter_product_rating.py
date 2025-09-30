import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MaxValueValidator(5.0), django.core.validators.MinValueValidator(0.0)]),
        ),
    ]