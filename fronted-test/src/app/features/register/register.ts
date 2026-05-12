import {
  Component,
  ChangeDetectorRef,
  EventEmitter,
  Output
} from '@angular/core';

import { CommonModule } from '@angular/common';

import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule
} from '@angular/forms';

import { timeout } from 'rxjs';

import { LoginService } from '../../service/loginservice/login_service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './register.html',
  styleUrls: ['./register.scss']
})
export class Register {

  @Output() goLogin = new EventEmitter<void>();

  form: FormGroup;

  msg = '';
  loading = false;

  constructor(
    private fb: FormBuilder,
    private loginService: LoginService,
    private cdr: ChangeDetectorRef
  ) {

    this.form = this.fb.group({
      username: [''],
      email: [''],
      identification: [''],
      password: [''],
    });

  }

  onSubmit(): void {

    const {
      username,
      email,
      identification,
      password
    } = this.form.value;

    if (
      !username ||
      !email ||
      !identification ||
      !password
    ) {
      this.msg = '⚠️ Todos los campos son obligatorios';
      return;
    }

    this.loading = true;
    this.msg = 'Registrando...';

    this.cdr.detectChanges();

    this.loginService
      .register(
        username,
        email,
        identification,
        password
      )
      .pipe(timeout(8000))
      .subscribe({

        next: () => {

          this.msg = '✅ Usuario creado correctamente';

          this.loading = false;

          this.cdr.detectChanges();

          setTimeout(() => {
            this.goLogin.emit();
          }, 800);

        },

        error: (err) => {

          console.error('REGISTER ERROR:', err);

          if (err?.name === 'TimeoutError') {
            this.msg = '⏱️ El servidor tardó demasiado';
          }
          else if (err?.status === 0) {
            this.msg = '🌐 No hay conexión con el servidor';
          }
          else if (err?.status === 400) {

            const msg = err?.error?.message || '';

            if (msg.includes('username')) {
              this.msg =
                '👤 Ese nombre de usuario ya está en uso';
            }
            else if (
              msg.includes('correo') ||
              msg.includes('email')
            ) {
              this.msg =
                '📧 Ese correo ya está registrado';
            }
            else if (
              msg.includes('identificación')
            ) {
              this.msg =
                '🆔 Esa identificación ya existe';
            }
            else {
              this.msg =
                '⚠️ No se pudo crear la cuenta';
            }

          }
          else if (err?.status === 409) {
            this.msg = '⚠️ Usuario ya registrado';
          }
          else {
            this.msg = '❌ Error al registrar';
          }

          this.loading = false;

          this.cdr.detectChanges();

        }

      });

  }
}