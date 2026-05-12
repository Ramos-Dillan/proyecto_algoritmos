import { Component, Input, OnChanges, OnInit, OnDestroy, SimpleChanges, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule, HttpHeaders } from '@angular/common/http';
import { Subscription } from 'rxjs';

interface User {
  id: number;
  username: string;
  email: string;
  identification: string;
  role?: string;
  is_active?: boolean;
}

@Component({
  selector: 'app-users',
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule],
  templateUrl: './users.html',
  styleUrls: ['./users.scss']
})
export class UsersComponent implements OnInit, OnChanges, OnDestroy {

  @Input() refresh: number = 0;

  users: User[] = [];
  errorMsg: string = '';
  loading: boolean = false;
  saving: boolean = false;

  editingUser: User | null = null;
  editForm: Partial<User> = {};

  private isLoadingRequest = false;
  private sub: Subscription | null = null;

  constructor(
    private http: HttpClient,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.isLoadingRequest = false;
    this.loadUsers();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['refresh'] && !changes['refresh'].firstChange) {
      this.loadUsers(true);
    }
  }

  ngOnDestroy(): void {
    this.sub?.unsubscribe();
    this.isLoadingRequest = false;
  }

  private getHeaders(): HttpHeaders | null {
    const token = localStorage.getItem('token');
    if (!token) {
      this.errorMsg = 'No hay token';
      return null;
    }
    return new HttpHeaders({ Authorization: `Bearer ${token}` });
  }

  loadUsers(force: boolean = false): void {
    if (this.isLoadingRequest && !force) return;

    const headers = this.getHeaders();
    if (!headers) return;

    this.isLoadingRequest = true;
    this.loading = true;
    this.errorMsg = '';
    this.cdr.detectChanges();

    this.sub?.unsubscribe();
    this.sub = this.http.get<{ data: User[] }>('http://localhost:5000/auth/users', { headers })
      .subscribe({
        next: (res) => {
          setTimeout(() => {
            this.users = res?.data ?? [];
            this.loading = false;
            this.isLoadingRequest = false;
            this.cdr.detectChanges();
          }, 0);
        },
        error: (err) => {
          console.error('Error cargando usuarios:', err);
          setTimeout(() => {
            this.errorMsg = 'Error cargando usuarios';
            this.loading = false;
            this.isLoadingRequest = false;
            this.cdr.detectChanges();
          }, 0);
        }
      });
  }

  openEdit(u: User): void {
    this.editingUser = u;
    this.editForm = {
      username: u.username,
      email: u.email,
      identification: u.identification,
      role: u.role,
      is_active: u.is_active
    };
    this.cdr.detectChanges();
  }

  closeEdit(): void {
    this.editingUser = null;
    this.editForm = {};
    this.cdr.detectChanges();
  }

  saveEdit(): void {
    if (!this.editingUser) return;

    const headers = this.getHeaders();
    if (!headers) return;

    this.saving = true;

    this.http.patch(
      `http://localhost:5000/auth/users/${this.editingUser.id}`,
      this.editForm,
      { headers }
    ).subscribe({
      next: () => {
        setTimeout(() => {
          const index = this.users.findIndex(u => u.id === this.editingUser!.id);
          if (index !== -1) {
            this.users[index] = { ...this.users[index], ...this.editForm };
          }
          this.saving = false;
          this.closeEdit();
          this.cdr.detectChanges();
        }, 0);
      },
      error: (err) => {
        console.error('Error actualizando usuario:', err);
        this.saving = false;
        this.cdr.detectChanges();
      }
    });
  }

  toggleActive(u: User): void {
    const headers = this.getHeaders();
    if (!headers) return;

    const newState = !Boolean(u.is_active);

    this.http.patch(
      `http://localhost:5000/auth/users/${u.id}`,
      { is_active: newState },
      { headers }
    ).subscribe({
      next: () => {
        setTimeout(() => {
          const index = this.users.findIndex(x => x.id === u.id);
          if (index !== -1) {
            this.users[index] = { ...this.users[index], is_active: newState };
          }
          this.cdr.detectChanges();
        }, 0);
      },
      error: (err) => {
        console.error('Error cambiando estado:', err);
      }
    });
  }

  deleteUser(u: User): void {
    const headers = this.getHeaders();
    if (!headers) return;

    const confirmDelete = confirm(`¿Eliminar usuario "${u.username}"?`);
    if (!confirmDelete) return;

    this.http.delete(
      `http://localhost:5000/auth/users/${u.id}`,
      { headers }
    ).subscribe({
      next: () => {
        setTimeout(() => {
          this.users = this.users.filter(x => x.id !== u.id);
          this.cdr.detectChanges();
        }, 0);
      },
      error: (err) => {
        console.error('Error eliminando usuario:', err);
      }
    });
  }
}