from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_favoritestock'),
    ]

    operations = [
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=20)),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('total', models.DecimalField(max_digits=10, decimal_places=2)),
                ('date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='investments', to='users.user')),
            ],
            options={
                'db_table': 'investments',
                'ordering': ['-created_at'],
            },
        ),
    ] 