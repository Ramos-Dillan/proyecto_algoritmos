import { Component, signal } from '@angular/core';
import { RouterOutlet, RouterModule } from '@angular/router';
import { AssistantComponent } from './features/assistant/assistant';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterModule, AssistantComponent],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('fronted-test');
}