import { TestBed } from '@angular/core/testing';

import { TokenKeeperService } from './token-keeper.service';

describe('TokenKeeperService', () => {
  let service: TokenKeeperService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TokenKeeperService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
