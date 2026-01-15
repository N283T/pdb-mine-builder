// Type definitions for libpq
declare module "libpq" {
  import { EventEmitter } from "events";

  interface PQNotice {
    relname: string;
    be_pid: number;
    extra: string;
  }

  class PQ extends EventEmitter {
    constructor();

    // Connection
    connect(params: string, callback?: (err: Error | null) => void): void;
    connectSync(params: string): void;
    finish(): void;

    // Query execution
    sendQuery(text: string): boolean;
    sendQueryParams(text: string, values: unknown[]): boolean;
    sendPrepare(
      statementName: string,
      text: string,
      nParams: number
    ): boolean;
    sendQueryPrepared(statementName: string, parameters: unknown[]): boolean;

    exec(text: string): void;
    execParams(text: string, values: unknown[]): void;
    prepare(statementName: string, text: string, nParams: number): void;
    execPrepared(statementName: string, parameters: unknown[]): void;

    // Result handling
    getResult(): boolean;
    resultStatus(): string;
    resultErrorMessage(): string;
    errorMessage(): string;
    nfields(): number;
    ntuples(): number;
    fname(columnIndex: number): string;
    ftype(columnIndex: number): number;
    getvalue(row: number, column: number): string;
    getisnull(row: number, column: number): boolean;

    // Async I/O
    consumeInput(): boolean;
    isBusy(): boolean;
    setNonBlocking(nonBlocking: boolean): boolean;
    flush(): number;
    writable(callback: () => void): void;
    startReader(): void;
    stopReader(): void;

    // Escaping
    escapeLiteral(value: string): string;
    escapeIdentifier(value: string): string;

    // Notifications
    notifies(): PQNotice | null;

    // COPY
    getCopyData(async: boolean): string | number;
    putCopyData(data: string | Buffer): number;
    putCopyEnd(errorMessage?: string): number;

    clear(): void;
  }

  export default PQ;
}
