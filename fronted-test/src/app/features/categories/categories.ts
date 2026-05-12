import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule, HttpHeaders } from '@angular/common/http';

interface Category {
  id: number;
  name: string;
}

@Component({
  selector: 'app-categories',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './categories.html',
  styleUrls: ['./categories.scss']
})
export class CategoriesComponent implements OnInit {

  categories: Category[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.getCategories();
  }

  getCategories() {

    const token = localStorage.getItem('token');

    console.log("TOKEN QUE SE ENVÍA:", token);

    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`
    });

    this.http.get<any>('http://localhost:5000/categories/getAll', { headers })
      .subscribe({
        next: (res) => {
          console.log("RESPUESTA BACKEND:", res);
          this.categories = res.data || [];
        },
        error: (err) => {
          console.error('Error cargando categorías', err);
        }
      });
  }
}