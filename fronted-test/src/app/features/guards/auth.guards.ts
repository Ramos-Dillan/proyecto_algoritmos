import { CanActivateChildFn, Router, UrlTree } from "@angular/router";
import { inject } from '@angular/core';
import { LoginService } from "../../service/loginservice/login_service";

export const authGuard: CanActivateChildFn = (_route, state): boolean | UrlTree => {

  const auth: LoginService = inject(LoginService);
  const router = inject(Router);

  if (auth.isAuthenticated()) {
    return true;
  }

  return router.createUrlTree(['/login'], {
    queryParams: { returnUrl: state.url }
  });
};