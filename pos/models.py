from django.db import models

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('Drink', 'Drink'),
        ('Food', 'Food'),
        ('Dessert', 'Dessert'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('cancelled', 'Cancelled'),
        ('finished',  'Finished'),
    ]

    table_number    = models.CharField(max_length=10)
    customer_name   = models.CharField(max_length=100)
    special_request = models.TextField(blank=True)
    ordered_at      = models.DateTimeField(auto_now_add=True)
    status          = models.CharField(
                        max_length=10,
                        choices=STATUS_CHOICES,
                        default='pending',
                    )

    def __str__(self):
        return f"Table {self.table_number} - {self.customer_name} ({self.ordered_at.strftime('%Y-%m-%d %H:%M')})"

    @property
    def total_amount(self):
        return sum(
            item.menu_item.price * item.quantity
            for item in self.items.all()
        )

class OrderItem(models.Model):
    order     = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, null=True, blank=True)
    quantity  = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.menu_item.name} x{self.quantity}"
