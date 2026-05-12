import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup } from '@angular/forms';
import { LoginService } from '../../service/loginservice/login_service';

@Component({
  selector: 'app-forgot-password',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './forgot-password.html',
  styleUrls: ['./forgot-password.scss']
})
export class ForgotPassword {

  form: FormGroup;

  loading = false;
  msg = '';

  constructor(
    private fb: FormBuilder,
    private loginService: LoginService
  ) {

    this.form = this.fb.group({
      email: ['']
    });

  }

  onSubmit(): void {

    const email = this.form.value.email;

    if (!email) {
      this.msg = '⚠️ Ingresa un correo';
      return;
    }

    this.loading = true;
    this.msg = '';

    this.loginService.forgotPassword(email).subscribe({

      next: (res) => {

        this.loading = false;

        this.msg =
          res?.message ||
          '✅ Si el correo existe, recibirás instrucciones';
      },

      error: (err) => {

        console.error(err);

        this.loading = false;

        this.msg =
          err?.error?.message ||
          '❌ Error enviando recuperación';
      }

    });

  }

}