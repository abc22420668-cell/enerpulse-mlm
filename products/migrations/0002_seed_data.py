"""
Seed initial EnerPulse products and categories.
"""
from django.db import migrations


def seed_data(apps, schema_editor):
    Category = apps.get_model('products', 'Category')
    Product = apps.get_model('products', 'Product')
    
    # Create default category
    cat, _ = Category.objects.get_or_create(
        slug='quantum-devices',
        defaults={
            'name': 'Quantum Devices',
            'name_en': 'Quantum Devices',
            'name_zh_hant': '量子設備',
            'name_zh_hans': '量子设备',
            'description': 'Premium quantum frequency technology products',
            'sort_order': 1,
            'is_active': True,
        }
    )
    
    # Product 1: Quantum Pulse Frequency Device
    Product.objects.get_or_create(
        sku='QPFD-001',
        defaults={
            'category': cat,
            'name': 'Quantum Pulse Frequency Device',
            'name_en': 'Quantum Pulse Frequency Device',
            'name_zh_hant': '量子脈衝頻率儀',
            'name_zh_hans': '量子脉冲频率仪',
            'description': 'Quantum frequency resonance technology — the core product powering your MLM journey. One unit = one membership share.',
            'description_en': 'Quantum frequency resonance technology — the core product powering your MLM journey. One unit = one membership share.',
            'description_zh_hant': '量子頻率共振技術 — 驅動您直銷事業的核心產品。每個單位 = 一份會員資格。',
            'description_zh_hans': '量子频率共振技术 — 驱动您直销事业的核心产品。每个单位 = 一份会员资格。',
            'slug': 'quantum-pulse-frequency-device',
            'price_usd': 1000.00,
            'pv': 750,
            'stock': 9999,
            'is_active': True,
            'is_featured': True,
        }
    )
    
    # Product 2: Quantum Wellness Bundle
    Product.objects.get_or_create(
        sku='QWB-002',
        defaults={
            'category': cat,
            'name': 'Quantum Wellness Bundle',
            'name_en': 'Quantum Wellness Bundle',
            'name_zh_hant': '量子健康組合包',
            'name_zh_hans': '量子健康组合包',
            'description': 'Complete wellness package: Quantum Pulse device plus premium health accessories.',
            'description_en': 'Complete wellness package: Quantum Pulse device plus premium health accessories.',
            'description_zh_hant': '全方位健康組合：量子脈衝頻率儀加上頂級健康配件。',
            'description_zh_hans': '全方位健康组合：量子脉冲频率仪加上顶级健康配件。',
            'slug': 'quantum-wellness-bundle',
            'price_usd': 1900.00,
            'pv': 1500,
            'stock': 500,
            'is_active': True,
            'is_featured': True,
        }
    )
    
    # Product 3: EnerPulse Membership
    Product.objects.get_or_create(
        sku='EPM-003',
        defaults={
            'category': cat,
            'name': 'EnerPulse Membership',
            'name_en': 'EnerPulse Membership',
            'name_zh_hant': 'EnerPulse 會員資格',
            'name_zh_hans': 'EnerPulse 会员资格',
            'description': 'Membership activation with Quantum Pulse device, starter kit, and full MLM benefits.',
            'description_en': 'Membership activation with Quantum Pulse device, starter kit, and full MLM benefits.',
            'description_zh_hant': '會員啟動方案：含量子脈衝頻率儀、入門套組及完整直銷獎勵權益。',
            'description_zh_hans': '会员启动方案：含量子脉冲频率仪、入门套组及完整直销奖励权益。',
            'slug': 'enerpulse-membership',
            'price_usd': 1000.00,
            'pv': 750,
            'stock': 9999,
            'is_active': True,
            'is_featured': True,
        }
    )


def reverse_seed(apps, schema_editor):
    Product = apps.get_model('products', 'Product')
    Product.objects.filter(sku__in=['QPFD-001', 'QWB-002', 'EPM-003']).delete()
    Category = apps.get_model('products', 'Category')
    Category.objects.filter(slug='quantum-devices').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('products', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(seed_data, reverse_seed),
    ]
