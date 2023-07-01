class Query {
  access_token!: string;
  refresh_token!: string;
  expires_at!: number;
}

export class Route {
  query!: Query;
}
