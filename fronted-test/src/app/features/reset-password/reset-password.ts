import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  ReactiveFormsModule,
  FormBuilder,
  FormGroup
} from '@angular/forms';

import { ActivatedRoute, Router } from '@angular/router';

import { LoginService } from '../../service/loginservice/login_service';

@Component({
  selector: 'app-reset-password',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './reset-password.html',
  styleUrls: ['./reset-password.scss']
})
export class ResetPassword {

  form: FormGroup;

  loading = false;
  msg = '';

  token = '';

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private loginService: LoginService
  ) {

    this.form = this.fb.group({
      password: ['']
    });

    this.route.queryParams.subscribe(params => {
      this.token = params['token'] || '';
    });

  }

  onSubmit(): void {

    const password = this.form.value.password;

    if (!password) {
      this.msg = '⚠️ Ingresa una contraseña';
      return;
    }

    this.loading = true;
    this.msg = '';

    this.loginService
      .resetPassword(this.token, password)
      .subscribe({

        next: (res) => {

          this.loading = false;

          this.msg =
            res?.message ||
            '✅ Contraseña actualizada';

          setTimeout(() => {
            this.router.navigateByUrl('/login');
          }, 1500);

        },

        error: (err) => {

          console.error(err);

          this.loading = false;

          this.msg =
            err?.error?.message ||
            '❌ Error restableciendo contraseña';
        }

      });

  }

}