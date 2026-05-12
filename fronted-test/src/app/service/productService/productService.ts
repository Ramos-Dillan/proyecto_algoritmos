import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap, map } from 'rxjs/operators';
import { environment } from '../../../environments/environment';

export interface Product {
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
}

type ApiResponse = {
  status: 'success' | 'error';
  message?: string;
  data?: any;
};

@Injectable({ providedIn: 'root' })
export class ProductService {
  private apiBaseUrl = `${environment.apiBaseURL}/product`;

  constructor(private http: HttpClient) {}

  getAllProducts() {
    return this.http.get<ApiResponse>(`${this.apiBaseUrl}/getAll`).pipe(
      tap((response) => {
        if (response.status === 'error') {
          console.error('Error fetching products:', response.message);
        }
      }),
      map((response) => (response.data || []) as Product[])
    );
  }

  filterProducts(params: Record<string, any>) {
    const query = new URLSearchParams();
    Object.keys(params || {}).forEach((k) => {
      if (params[k] !== undefined && params[k] !== null && params[k] !== '') {
        query.set(k, String(params[k]));
      }
    });

    const url = `${this.apiBaseUrl}/filter${query.toString() ? '?' + query.toString() : ''}`;

    return this.http.get<ApiResponse>(url).pipe(
      tap((response) => {
        if (response.status === 'error') {
          console.error('Error filtering products:', response.message);
        }
      }),
      map((response) => {
        const data = response.data || { items: [], total: 0 };
        return {
          items: (data.items || []) as Product[],
          total: data.total || 0
        };
      })
    );
  }

  getProductById(id: number) {
    return this.http.get<ApiResponse>(`${this.apiBaseUrl}/get/${id}`).pipe(
      map((res) => res.data as Product)
    );
  }

  updateProduct(id: number, data: Partial<Product>) {
    return this.http.put<ApiResponse>(`${this.apiBaseUrl}/updateProduct/${id}`, data).pipe(
      map((res) => res.data)
    );
  }

  toggleActive(id: number, is_active: boolean) {
    return this.http.patch<ApiResponse>(`${this.apiBaseUrl}/toggleActive/${id}`, { is_active }).pipe(
      map((res) => res.data)
    );
  }
}