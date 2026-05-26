import { Component, OnInit, ChangeDetectorRef, NgZone } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule, HttpHeaders } from '@angular/common/http';

import { ProductsComponent } from '../products/products';
import { ProductDetail } from '../products/product-detail';
import { UsersComponent } from '../users/users';
import { Dashboard } from '../dashboard/dashboard';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    FormsModule,
    HttpClientModule,
    ProductsComponent,
    ProductDetail,
    UsersComponent,
    Dashboard
  ],
  templateUrl: './home.html',
  styleUrls: ['./home.scss']
})
export class HomeComponent implements OnInit {

  userName = 'Full Name';
  userRole: string = '';
  userId: number | null = null;

  menuOpen = true;
  showUserMenu = false;
  showEditModal = false;

  editForm = {
    username: '',
    email: '',
    password: ''
  };
  editError = '';
  editSuccess = '';
  editSaving = false;

  vista: string = 'home';
  selectedProductId: number | null = null;

  refreshDashboard = 0;
  refreshUsers = 0;

  constructor(
    private router: Router,
    private http: HttpClient,
    private cdr: ChangeDetectorRef,
    private ngZone: NgZone
  ) {
    const user = JSON.parse(localStorage.getItem('my_user') || '{}');
    this.userName = user.username || 'Full Name';
    this.userRole = user.role || '';
    this.userId = user.id || null;
  }

  toggleMenu() {
    this.menuOpen = !this.menuOpen;
  }

  toggleUserMenu() {
    this.showUserMenu = !this.showUserMenu;
  }

  cambiarVista(event: Event, vista: string) {
    event.preventDefault();
    event.stopPropagation();
    this.vista = vista;
    this.selectedProductId = null;
    if (vista === 'dashboard') this.refreshDashboard++;
    if (vista === 'users') this.refreshUsers++;
  }

  verDetalleProducto(id: number) {
    this.selectedProductId = id;
    this.vista = 'product-detail';
  }

  volverAProductos() {
    this.selectedProductId = null;
    this.vista = 'products';
  }

  editar() {
    const user = JSON.parse(localStorage.getItem('my_user') || '{}');
    this.editForm = {
      username: user.username || '',
      email: user.email || '',
      password: ''
    };
    this.editError = '';
    this.editSuccess = '';
    this.showEditModal = true;
    this.showUserMenu = false;
  }

  closeEditModal() {
    this.showEditModal = false;
    this.editError = '';
    this.editSuccess = '';
  }

  saveEdit() {
    if (!this.userId) return;

    const token = localStorage.getItem('token');
    if (!token) return;

    const headers = new HttpHeaders({ Authorization: `Bearer ${token}` });

    const body: any = {
      username: this.editForm.username,
      email: this.editForm.email
    };
    if (this.editForm.password.trim()) {
      body.password = this.editForm.password;
    }

    this.editSaving = true;
    this.editError = '';
    this.editSuccess = '';

    this.http.patch(
      `http://localhost:5000/auth/users/${this.userId}`,
      body,
      { headers }
    ).subscribe({
      next: () => {
        this.ngZone.run(() => {
          const user = JSON.parse(localStorage.getItem('my_user') || '{}');
          user.username = this.editForm.username;
          user.email = this.editForm.email;
          localStorage.setItem('my_user', JSON.stringify(user));
          this.userName = this.editForm.username;
          this.editSaving = false;
          this.editSuccess = '¡Perfil actualizado correctamente!';
          this.cdr.detectChanges();
          setTimeout(() => {
            this.closeEditModal();
            this.cdr.detectChanges();
          }, 1500);
        });
      },
      error: (err) => {
        this.ngZone.run(() => {
          console.error(err);
          this.editError = 'Error al actualizar. Intenta de nuevo.';
          this.editSaving = false;
          this.cdr.detectChanges();
        });
      }
    });
  }

  abrirAsistente() {
    window.dispatchEvent(new CustomEvent('openChat'));
  }

  logout() {
    localStorage.clear();
    this.router.navigateByUrl('/login', { replaceUrl: true });
  }

  ngOnInit(): void {
    const token = localStorage.getItem('token');
    if (!token) {
      this.router.navigateByUrl('/login', { replaceUrl: true });
    }
  }
}

export { HomeComponent as Home };