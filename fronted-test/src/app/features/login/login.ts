import { Component, ChangeDetectorRef, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { firstValueFrom, timeout } from 'rxjs';
import { LoginService } from '../../service/loginservice/login_service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './login.html',
  styleUrls: ['./login.scss']
})
export class Login {
  @Output() goRegister = new EventEmitter<void>();

  form: FormGroup;
  loading = false;
  errorMsg = '';

  constructor(
    private fb: FormBuilder,
    private loginService: LoginService,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {
    this.form = this.fb.group({
      email: [''],
      password: [''],
    });
  }

  async onSubmit(): Promise<void> {
    const { email, password } = this.form.value;

    if (!email || !password) {
      this.errorMsg = '⚠️ Completa todos los campos';
      return;
    }

    this.loading = true;
    this.errorMsg = '';
    this.cdr.detectChanges();

    try {
      await firstValueFrom(
        this.loginService.login(email, password).pipe(timeout(5000))
      );

      this.router.navigateByUrl('/home');
    } catch (err: any) {
      console.error('login Error', err);

      if (err?.name === 'TimeoutError') {
        this.errorMsg = '⏱️ El servidor tardó demasiado';
      } else if (err?.status === 0) {
        this.errorMsg = '🌐 No hay conexión con el servidor';
      } else if (err?.status === 401) {
        this.errorMsg = '❌ Usuario o contraseña incorrectos';
      } else {
        this.errorMsg = err?.error?.message || '❌ Error inesperado';
      }

      this.cdr.detectChanges();
    } finally {
      this.loading = false;
      this.cdr.detectChanges();
    }
  }
}