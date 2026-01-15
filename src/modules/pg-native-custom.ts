/* eslint-disable @typescript-eslint/no-explicit-any */
const originalLog = console.log;
console.log = function () {}; // workaround to old libpq being noisy
import Libpq from "libpq";
console.log = originalLog;

import { EventEmitter } from "events";
import * as util from "util";
import types from "pg-types";

import { Deferred } from "./general.js";

// Type definitions
type TypeParser = (value: string) => unknown;
type QueryCallback = (
  err: Error | null | undefined,
  rows?: unknown[],
  results?: QueryResult | QueryResult[]
) => void;

interface TypesModule {
  setTypeParser(oid: number, parser: TypeParser): void;
  getTypeParser(oid: number): TypeParser;
}

interface QueryResult {
  rows?: unknown[][];
  columns?: string[];
  [field: string]: unknown;
}

interface ClientConfig {
  types?: TypesModule;
}

// Configure type parsers
types.setTypeParser(20, BigInt);
types.setTypeParser(1082, (date: string) => date); // don't process date object...
types.setTypeParser(1184, (x: string) => new Date(x)); // fix timezone
types.setTypeParser(1114, (x: string) => new Date(x)); // fix timezone

export interface Client extends EventEmitter {
  pq: Libpq;
  _reading: boolean;
  _read: () => void;
  _types: TypesModule;
  _resultCount: number;
  _rows: unknown[] | undefined;
  _results: QueryResult | QueryResult[] | undefined;
  _queryCallback: QueryCallback | undefined;
  _queryError: Error | undefined;
  rowMode: number;

  // Methods
  connect(params: string): Promise<void>;
  query(
    text: string,
    values?: unknown[] | QueryCallback,
    cb?: QueryCallback
  ): Promise<QueryResult | QueryResult[]> | undefined;
  prepare(
    statementName: string,
    text: string,
    nParams: number,
    cb?: QueryCallback
  ): Promise<QueryResult | QueryResult[]> | undefined;
  execute(
    statementName: string,
    parameters: unknown[],
    cb?: QueryCallback
  ): Promise<QueryResult | QueryResult[]> | undefined;
  escapeLiteral(value: string): string;
  escapeIdentifier(value: string): string;
  end(cb?: QueryCallback): Promise<void> | undefined;
  _readError(message?: string): void;
  _stopReading(): void;
  _consumeQueryResults(
    pq: Libpq
  ): QueryResult | Generator<unknown[], void, unknown>;
  _emitResult(pq: Libpq): string;
  _startReading(): void;
  _awaitResult(cb: QueryCallback): void;
  _waitForDrain(pq: Libpq, cb: (err?: Error) => void): void;
  _dispatchQuery(pq: Libpq, fn: () => boolean, cb: (err?: Error) => void): void;
  _onResult(result: QueryResult): void;
  _onReadyForQuery(): void;
}

export interface ClientConstructor {
  new (config?: ClientConfig): Client;
  (config?: ClientConfig): Client;
}

export const Client = function (
  this: Client | void,
  config?: ClientConfig
): Client {
  if (!(this instanceof Client)) {
    return new (Client as ClientConstructor)(config);
  }

  config = config || {};

  EventEmitter.call(this as unknown as EventEmitter);
  this.pq = new Libpq();
  this._reading = false;
  this._read = (Client.prototype._read as () => void).bind(this);

  // allow custom type conversion to be passed in
  this._types = config.types || types;

  this._resultCount = 0;
  this._rows = undefined;
  this._results = undefined;

  // lazy start the reader if notifications are listened for
  // this way if you only run sync queries you wont block
  // the event loop artificially
  this.on("newListener", (event: string) => {
    if (event !== "notification") return;
    this._startReading();
  });

  this.on("result", (Client.prototype._onResult as (result: QueryResult) => void).bind(this));
  this.on("readyForQuery", (Client.prototype._onReadyForQuery as () => void).bind(this));

  return this;
} as unknown as ClientConstructor;

util.inherits(Client, EventEmitter);

Client.prototype.connect = function (
  this: Client,
  params: string
): Promise<void> {
  const deferred = new Deferred<void>();
  const cb = function (err: Error | null) {
    if (err) deferred.reject(err);
    else deferred.resolve();
  };
  this.pq.connect(params, cb);
  return deferred.promise;
};

Client.prototype.query = function (
  this: Client,
  text: string,
  values?: unknown[] | QueryCallback,
  cb?: QueryCallback
): Promise<QueryResult | QueryResult[]> | undefined {
  let queryFn: () => boolean;
  let promise: Promise<QueryResult | QueryResult[]> | undefined;

  if (typeof values === "function" || values === undefined) {
    cb = values as QueryCallback | undefined;
    queryFn = () => this.pq.sendQuery(text);
  } else {
    queryFn = () => this.pq.sendQueryParams(text, values);
  }

  if (cb === undefined) {
    const deferred = new Deferred<QueryResult | QueryResult[]>();
    promise = deferred.promise;
    cb = function (err, _rows, results) {
      if (err) deferred.reject(err);
      else deferred.resolve(results!);
    };
  }

  const finalCb = cb;
  this._dispatchQuery(this.pq, queryFn, (err?: Error) => {
    if (err) return finalCb(err);
    this._awaitResult(finalCb);
  });

  return promise;
};

Client.prototype.prepare = function (
  this: Client,
  statementName: string,
  text: string,
  nParams: number,
  cb?: QueryCallback
): Promise<QueryResult | QueryResult[]> | undefined {
  let promise: Promise<QueryResult | QueryResult[]> | undefined;
  const fn = () => this.pq.sendPrepare(statementName, text, nParams);

  if (cb === undefined) {
    const deferred = new Deferred<QueryResult | QueryResult[]>();
    promise = deferred.promise;
    cb = function (err, _rows, results) {
      if (err) deferred.reject(err);
      else deferred.resolve(results!);
    };
  }

  const finalCb = cb;
  this._dispatchQuery(this.pq, fn, (err?: Error) => {
    if (err) return finalCb(err);
    this._awaitResult(finalCb);
  });

  return promise;
};

Client.prototype.execute = function (
  this: Client,
  statementName: string,
  parameters: unknown[],
  cb?: QueryCallback
): Promise<QueryResult | QueryResult[]> | undefined {
  let promise: Promise<QueryResult | QueryResult[]> | undefined;

  const fn = () => this.pq.sendQueryPrepared(statementName, parameters);

  if (cb === undefined) {
    const deferred = new Deferred<QueryResult | QueryResult[]>();
    promise = deferred.promise;
    cb = function (err, _rows, results) {
      if (err) deferred.reject(err);
      else deferred.resolve(results!);
    };
  }

  const finalCb = cb;
  this._dispatchQuery(this.pq, fn, (err?: Error) => {
    if (err) return finalCb(err);
    this._awaitResult(finalCb);
  });

  return promise;
};

Client.prototype.escapeLiteral = function (this: Client, value: string): string {
  return this.pq.escapeLiteral(value);
};

Client.prototype.escapeIdentifier = function (
  this: Client,
  value: string
): string {
  return this.pq.escapeIdentifier(value);
};

Client.prototype.end = function (
  this: Client,
  cb?: QueryCallback
): Promise<void> | undefined {
  let promise: Promise<void> | undefined;
  if (cb === undefined) {
    const deferred = new Deferred<void>();
    promise = deferred.promise;
    cb = function (err) {
      if (err) deferred.reject(err);
      else deferred.resolve();
    };
  }

  this._stopReading();
  this.pq.finish();
  if (cb) setImmediate(cb as () => void);
  return promise;
};

Client.prototype._readError = function (this: Client, message?: string): void {
  const err = new Error(message || this.pq.errorMessage());
  this.emit("error", err);
};

Client.prototype._stopReading = function (this: Client): void {
  if (!this._reading) return;
  this._reading = false;
  this.pq.stopReader();
  this.pq.removeListener("readable", this._read);
};

Client.prototype._consumeQueryResults = function (
  this: Client,
  pq: Libpq
): QueryResult | Generator<unknown[], void, unknown> {
  if (this.rowMode === -1) return yieldResults(pq, this._types);
  return buildResult(pq, this._types, this.rowMode);
};

Client.prototype._emitResult = function (this: Client, pq: Libpq): string {
  const status = pq.resultStatus();
  switch (status) {
    case "PGRES_FATAL_ERROR":
      this._queryError = new Error(this.pq.resultErrorMessage());
      break;

    case "PGRES_TUPLES_OK":
    case "PGRES_COMMAND_OK":
    case "PGRES_EMPTY_QUERY": {
      const result = this._consumeQueryResults(this.pq);
      this.emit("result", result);
      break;
    }

    case "PGRES_COPY_OUT":
    case "PGRES_COPY_BOTH": {
      break;
    }

    default:
      this._readError("unrecognized command status: " + status);
      break;
  }
  return status;
};

// called when libpq is readable
Client.prototype._read = function (this: Client): void {
  const pq = this.pq;
  // read waiting data from the socket
  // e.g. clear the pending 'select'
  if (!pq.consumeInput()) {
    // if consumeInput returns false
    // than a read error has been encountered
    return this._readError();
  }

  // check if there is still outstanding data
  // if so, wait for it all to come in
  if (pq.isBusy()) {
    return;
  }

  // load our result object

  while (pq.getResult()) {
    const resultStatus = this._emitResult(this.pq);

    // if the command initiated copy mode we need to break out of the read loop
    // so a substream can begin to read copy data
    if (resultStatus === "PGRES_COPY_BOTH" || resultStatus === "PGRES_COPY_OUT") {
      break;
    }

    // if reading multiple results, sometimes the following results might cause
    // a blocking read. in this scenario yield back off the reader until libpq is readable
    if (pq.isBusy()) {
      return;
    }
  }

  this.emit("readyForQuery");

  let notice = this.pq.notifies();
  while (notice) {
    this.emit("notification", notice);
    notice = this.pq.notifies();
  }
};

// ensures the client is reading and
// everything is set up for async io
Client.prototype._startReading = function (this: Client): void {
  if (this._reading) return;
  this._reading = true;
  this.pq.on("readable", this._read);
  this.pq.startReader();
};

Client.prototype._awaitResult = function (
  this: Client,
  cb: QueryCallback
): void {
  this._queryCallback = cb;
  this._startReading();
};

// wait for the writable socket to drain
Client.prototype._waitForDrain = function (
  this: Client,
  pq: Libpq,
  cb: (err?: Error) => void
): void {
  const res = pq.flush();
  // res of 0 is success
  if (res === 0) return cb();

  // res of -1 is failure
  if (res === -1) return cb(new Error(pq.errorMessage()));

  // otherwise outgoing message didn't flush to socket
  // wait for it to flush and try again
  // you cannot read & write on a socket at the same time
  pq.writable(() => {
    this._waitForDrain(pq, cb);
  });
};

// send an async query to libpq and wait for it to
// finish writing query text to the socket
Client.prototype._dispatchQuery = function (
  this: Client,
  pq: Libpq,
  fn: () => boolean,
  cb: (err?: Error) => void
): void {
  this._stopReading();
  const success = pq.setNonBlocking(true);
  if (!success) return cb(new Error("Unable to set non-blocking to true"));
  const sent = fn();
  if (!sent)
    return cb(
      new Error(pq.errorMessage() || "Something went wrong dispatching the query")
    );
  this._waitForDrain(pq, cb);
};

Client.prototype._onResult = function (this: Client, result: QueryResult): void {
  if (this._resultCount === 0) {
    this._results = result;
    this._rows = result.rows;
  } else if (this._resultCount === 1) {
    this._results = [this._results as QueryResult, result];
    this._rows = [this._rows, result.rows];
  } else {
    (this._results as QueryResult[]).push(result);
    (this._rows as unknown[]).push(result.rows);
  }
  this._resultCount++;
};

Client.prototype._onReadyForQuery = function (this: Client): void {
  // remove instance callback
  const cb = this._queryCallback;
  this._queryCallback = undefined;

  // remove instance query error
  const err = this._queryError;
  this._queryError = undefined;

  // remove instance rows
  const rows = this._rows;
  this._rows = undefined;

  // remove instance results
  const results = this._results;
  this._results = undefined;

  this._resultCount = 0;

  if (cb) {
    cb(err, (rows as unknown[]) || [], results);
  }
};

function* yieldResults(
  pq: Libpq,
  typesModule: TypesModule
): Generator<unknown[], void, unknown> {
  const nfields = pq.nfields();
  const nrows = pq.ntuples();
  for (let i = 0; i < nrows; i++) {
    const row: unknown[] = [];
    for (let j = 0; j < nfields; j++) {
      const func = typesModule.getTypeParser(pq.ftype(j));
      const rawValue = pq.getvalue(i, j);
      if (rawValue === "" && pq.getisnull(i, j)) row.push(null);
      else row.push(func(rawValue));
    }
    yield row;
  }
}

function buildResult(
  pq: Libpq,
  typesModule: TypesModule,
  rowMode: number
): QueryResult {
  const nfields = pq.nfields();
  const nrows = pq.ntuples();
  const table: QueryResult = {};

  if (rowMode) {
    table.rows = [];
    table.columns = [];
    for (let j = 0; j < nfields; j++) table.columns.push(pq.fname(j));
    for (let i = 0; i < nrows; i++) {
      const row: unknown[] = [];
      table.rows.push(row);
      for (let j = 0; j < nfields; j++) {
        const func = typesModule.getTypeParser(pq.ftype(j));
        const rawValue = pq.getvalue(i, j);
        if (rawValue === "" && pq.getisnull(i, j)) row.push(null);
        else row.push(func(rawValue));
      }
    }
    return table;
  }

  for (let j = 0; j < nfields; j++) {
    const col: unknown[] = [];
    table[pq.fname(j)] = col;
    const func = typesModule.getTypeParser(pq.ftype(j));
    for (let i = 0; i < nrows; i++) {
      const rawValue = pq.getvalue(i, j);
      if (rawValue === "" && pq.getisnull(i, j)) col.push(null);
      else col.push(func(rawValue));
    }
  }
  return table;
}
