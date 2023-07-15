export interface Step {
  currentStep: {
    value: {
      created_after_month: string;
      created_before_month: string;
    };
  };
  targetStep: {
    stepName: string;
  };
  delta: number;
}

export interface Playlist {
  playlistInformation: {
    name: string;
    description: string;
    display: boolean;
  };
  filters: Filters;
}

export interface Filters {
  genres: Array<string>;
  artists: Array<string>;
  created_after_month: string;
  created_before_month: string;
}

export interface Artist {
  name: string;
  external_url: string;
}

export interface Song {
  song_name: string;
  song_url: string;
  artists: Array<Artist>;
  preview_url: string;
}

export interface Genre_Options {
  label: string;
  options: Array<Genre>;
}

export interface Artist_Options {
  label: string;
  value: string;
}

export interface Genre {
  label: string;
  value: string;
}
