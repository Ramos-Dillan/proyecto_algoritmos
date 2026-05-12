import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';

interface Role {
  id: number;
  name: string;
}

@Component({
  selector: 'app-roles',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './roles.html',
  styleUrls: ['./roles.scss']
})
export class RolesComponent {

  roles: Role[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.getRoles();
  }

  getRoles() {
    this.http.get<any>('http://localhost:5000/api/roles')
      .subscribe({
        next: (res) => {
          this.roles = res.data;
        },
        error: (err) => {
          console.error('Error cargando roles', err);
        }
      });
  }
}