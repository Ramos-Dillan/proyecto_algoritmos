import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Login } from '../../login/login';
import { Register } from '../../register/register';

@Component({
  selector: 'app-auth-shell',
  standalone: true,
  imports: [CommonModule, Login, Register],
  templateUrl: './auth-shell.html',
  styleUrls: ['./auth-shell.scss']
})
export class AuthShellComponent {
  showRegister = false;

  togglePanel(): void {
    this.showRegister = !this.showRegister;
  }
}