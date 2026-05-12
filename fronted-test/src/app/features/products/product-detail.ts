import { Component, OnInit, OnChanges, SimpleChanges, Input, Output, EventEmitter, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ProductService } from '../../service/productService/productService';

@Component({
  selector: 'app-product-detail',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './product-detail.html',
  styleUrls: ['./product-detail.scss']
})
export class ProductDetail implements OnInit, OnChanges {

  @Input() productId: number | null = null;
  @Output() volver = new EventEmitter<void>();

  product: any = null;
  loading = false;
  error = '';
  editingImage = false;
  newImageUrl = '';
  savingImage = false;

  constructor(
    private productService: ProductService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    if (this.productId) this.loadProduct(this.productId);
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['productId'] && this.productId) {
      this.loadProduct(this.productId);
    }
  }

  loadProduct(id: number) {
    this.loading = true;
    this.error = '';
    this.product = null;
    this.cdr.detectChanges();

    this.productService.getProductById(id).subscribe({
      next: (data) => {
        setTimeout(() => {
          this.product = data;
          this.newImageUrl = data.image_url || '';
          this.loading = false;
          this.cdr.detectChanges();
        }, 0);
      },
      error: () => {
        setTimeout(() => {
          this.error = 'Error cargando producto';
          this.loading = false;
          this.cdr.detectChanges();
        }, 0);
      }
    });
  }

  saveImage() {
    if (!this.newImageUrl.trim()) return;
    this.savingImage = true;

    this.productService.updateProduct(this.product.id, {
      ...this.product,
      image_url: this.newImageUrl
    }).subscribe({
      next: () => {
        setTimeout(() => {
          this.product.image_url = this.newImageUrl;
          this.editingImage = false;
          this.savingImage = false;
          this.cdr.detectChanges();
        }, 0);
      },
      error: () => {
        this.savingImage = false;
      }
    });
  }

  back() {
    this.volver.emit();
  }
}

export { ProductDetail as ProductDetailComponent };