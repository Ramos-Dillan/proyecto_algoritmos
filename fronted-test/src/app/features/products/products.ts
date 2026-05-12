import {
  ChangeDetectionStrategy,
  ChangeDetectorRef,
  Component,
  EventEmitter,
  OnInit,
  Output
} from '@angular/core';

import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ProductService } from '../../service/productService/productService';

interface Product {
  id: number;
  generic_name: string;
  commercial_name: string;
  concentration: string;
  pharmaceutical_form: string;
  dosage: string;
  notes: string;
  is_active: boolean;
  therapeutic_group: string;
  laboratory: string;
  category: string;
  image_url?: string;
  therapeutic_group_id?: number;
  laboratory_id?: number;
  category_id?: number;
}

@Component({
  selector: 'app-products',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './products.html',
  styleUrls: ['./products.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ProductsComponent implements OnInit {

  products: Product[] = [];
  allProducts: Product[] = [];

  loading = false;
  errorMessage = '';
  searchText = '';
  saving = false;

  editingProduct: Product | null = null;
  editForm: any = {};

  @Output() verDetalle = new EventEmitter<number>();

  isAdmin = false;
  isViewer = false;

  constructor(
    private productService: ProductService,
    private cdr: ChangeDetectorRef
  ) {
    const user = JSON.parse(localStorage.getItem('my_user') || '{}');
    const role = user.role?.toLowerCase();
    this.isAdmin = role === 'admin';
    this.isViewer = role === 'medico' || role === 'estudiante';
  }

  ngOnInit(): void {
    this.loadAll();
  }

  trackByProductId(index: number, p: Product): number {
    return p.id;
  }

  loadAll(): void {
    this.loading = true;
    this.errorMessage = '';
    this.cdr.markForCheck();

    this.productService.getAllProducts().subscribe({
      next: (items) => {
        this.allProducts = [...((items as Product[]) || [])];
        this.products = [...this.allProducts];
        this.loading = false;
        this.cdr.markForCheck();
      },
      error: () => {
        this.errorMessage = 'Error cargando productos.';
        this.loading = false;
        this.cdr.markForCheck();
      }
    });
  }

  getProducts(): void {
    this.searchText = '';
    this.products = [...this.allProducts];
    this.cdr.markForCheck();
  }

  doFilter(): void {
    const text = this.searchText.trim().toLowerCase();
    if (!text) {
      this.products = [...this.allProducts];
      this.cdr.markForCheck();
      return;
    }
    this.products = this.allProducts.filter((p: any) =>
      Object.values(p).some((value: any) =>
        String(value ?? '').toLowerCase().includes(text)
      )
    );
    this.cdr.markForCheck();
  }

  openEdit(p: Product): void {
    this.editingProduct = { ...p };
    this.editForm = {
      generic_name: p.generic_name,
      commercial_name: p.commercial_name,
      concentration: p.concentration,
      pharmaceutical_form: p.pharmaceutical_form,
      dosage: p.dosage,
      notes: p.notes,
      is_active: p.is_active,
      therapeutic_group_id: p.therapeutic_group_id,
      laboratory_id: p.laboratory_id,
      image_url: p.image_url ?? null
    };
    this.saving = false;
    this.cdr.markForCheck();
  }

  closeEdit(): void {
    this.editingProduct = null;
    this.editForm = {};
    this.saving = false;
    this.cdr.markForCheck();
  }

  saveEdit(): void {
    if (!this.editingProduct || this.saving) return;

    this.saving = true;
    this.cdr.markForCheck();

    const currentId = this.editingProduct.id;

    this.productService.updateProduct(currentId, this.editForm).subscribe({
      next: () => {
        this.products = this.products.map((p) =>
          p.id === currentId ? { ...p, ...this.editForm } : p
        );
        this.allProducts = this.allProducts.map((p) =>
          p.id === currentId ? { ...p, ...this.editForm } : p
        );
        this.saving = false;
        this.editingProduct = null;
        this.editForm = {};
        this.cdr.markForCheck();
      },
      error: (err) => {
        console.error('Error guardando producto:', err);
        this.saving = false;
        this.cdr.markForCheck();
      }
    });
  }

  toggleActive(p: Product): void {
    const newState = !p.is_active;
    this.productService.toggleActive(p.id, newState).subscribe({
      next: () => {
        this.products = this.products.map((x) =>
          x.id === p.id ? { ...x, is_active: newState } : x
        );
        this.allProducts = this.allProducts.map((x) =>
          x.id === p.id ? { ...x, is_active: newState } : x
        );
        this.cdr.markForCheck();
      },
      error: (err) => {
        console.error('Error toggling active', err);
        this.cdr.markForCheck();
      }
    });
  }
}