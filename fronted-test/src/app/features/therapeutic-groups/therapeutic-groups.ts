import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';

interface TherapeuticGroup {
  id: number;
  name: string;
  mechanism: string;
  description: string;
}

@Component({
  selector: 'app-therapeutic-groups',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './therapeutic-groups.html',
  styleUrls: ['./therapeutic-groups.scss']
})
export class TherapeuticGroupsComponent implements OnInit {

  therapeutic_groups: TherapeuticGroup[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.getGroups();
  }

  getGroups(): void {
    this.http.get<TherapeuticGroup[]>('http://localhost:8000/therapeutic_groups')
      .subscribe({
        next: (data) => {
          this.therapeutic_groups = data;
        },
        error: (err) => {
          console.error('Error cargando grupos', err);
        }
      });
  }
}