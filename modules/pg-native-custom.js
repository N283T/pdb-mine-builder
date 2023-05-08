const baka = console.log; console.log = function() {}; // workaround to old libpq being noisy
const Libpq = (await import('libpq')).default;
console.log = baka;
const EventEmitter = (await import('events')).EventEmitter;
const util = await import('util');
const assert = await import('assert');
const types = (await import('pg-types')).default;

const general = await import("./general.js");

types.setTypeParser(20, BigInt);
types.setTypeParser(1082, date => date); // don't process date object...
types.setTypeParser(1184, function(x) { // fix timezone
  return new Date(x);
});
types.setTypeParser(1114, function(x) { // fix timezone
  return new Date(x);
});

export function Client(config) {
  if (!(this instanceof Client)) {
    return new Client(config)
  }

  config = config || {}

  EventEmitter.call(this)
  this.pq = new Libpq()
  this._reading = false
  this._read = this._read.bind(this)

  // allow custom type converstion to be passed in
  this._types = config.types || types

  this._resultCount = 0
  this._rows = undefined
  this._results = undefined

  // lazy start the reader if notifications are listened for
  // this way if you only run sync queries you wont block
  // the event loop artificially
  this.on('newListener', (event) => {
    if (event !== 'notification') return
    this._startReading()
  })

  this.on('result', this._onResult.bind(this))
  this.on('readyForQuery', this._onReadyForQuery.bind(this))
}

util.inherits(Client, EventEmitter)

Client.prototype.connect = function(params) {
  var baka = new general.Deferred();
  var promise = baka.promise;
  var cb = function(err, rows, results) {
    if (err) baka.reject(err);
    baka.resolve(results);
  }
  this.pq.connect(params, cb)
  return promise;
}

Client.prototype.query = function (text, values, cb) {
  var queryFn, promise;

  if (typeof values === 'function' || values === undefined) {
    cb = values
    queryFn = function () { return self.pq.sendQuery(text) }
  } else {
    queryFn = function () { return self.pq.sendQueryParams(text, values) }
  }

  if (cb === undefined) {
    var baka = new general.Deferred();
    promise = baka.promise;
    cb = function(err, rows, results) {
      if (err) baka.reject(err);
      baka.resolve(results);
    }
  }

  var self = this
  self._dispatchQuery(self.pq, queryFn, function (err) {
    if (err) return cb(err)

    self._awaitResult(cb)
  })
  
  return promise;
}

Client.prototype.prepare = function (statementName, text, nParams, cb) {
  var self = this; var promise;
  var fn = function () {
    return self.pq.sendPrepare(statementName, text, nParams)
  }
  
  if (cb === undefined) {
    var baka = new general.Deferred();
    promise = baka.promise;
    cb = function(err, rows, results) {
      if (err) baka.reject(err);
      baka.resolve(results);
    }
  }

  self._dispatchQuery(self.pq, fn, function (err) {
    if (err) return cb(err)
    self._awaitResult(cb)
  })
  
  return promise;
}

Client.prototype.execute = function (statementName, parameters, cb) {
  var self = this; var promise;

  var fn = function () {
    return self.pq.sendQueryPrepared(statementName, parameters)
  }
  
  if (cb === undefined) {
    var baka = new general.Deferred();
    promise = baka.promise;
    cb = function(err, rows, results) {
      if (err) baka.reject(err);
      baka.resolve(results);
    }
  }

  self._dispatchQuery(self.pq, fn, function (err, rows) {
    if (err) return cb(err)
    self._awaitResult(cb)
  })
  
  return promise;
}

Client.prototype.escapeLiteral = function (value) {
  return this.pq.escapeLiteral(value)
}

Client.prototype.escapeIdentifier = function (value) {
  return this.pq.escapeIdentifier(value)
}

Client.prototype.end = function (cb) {
  var promise;
  if (cb === undefined) {
    var baka = new general.Deferred();
    promise = baka.promise;
    cb = function(err, rows, results) {
      if (err) baka.reject(err);
      baka.resolve(results);
    }
  }
  
  this._stopReading()
  this.pq.finish()
  if (cb) setImmediate(cb)
  return promise;
}

Client.prototype._readError = function (message) {
  var err = new Error(message || this.pq.errorMessage())
  this.emit('error', err)
}

Client.prototype._stopReading = function () {
  if (!this._reading) return
  this._reading = false
  this.pq.stopReader()
  this.pq.removeListener('readable', this._read)
}

Client.prototype._consumeQueryResults = function (pq) {
  if (this.rowMode == -1) return yieldResults(pq, this._types);
  return buildResult(pq, this._types, this.rowMode)
}

Client.prototype._emitResult = function (pq) {
  var status = pq.resultStatus()
  switch (status) {
    case 'PGRES_FATAL_ERROR':
      this._queryError = new Error(this.pq.resultErrorMessage())
      break

    case 'PGRES_TUPLES_OK':
    case 'PGRES_COMMAND_OK':
    case 'PGRES_EMPTY_QUERY':
      const result = this._consumeQueryResults(this.pq)
      this.emit('result', result)
      break

    case 'PGRES_COPY_OUT':
    case 'PGRES_COPY_BOTH': {
      break
    }

    default:
      this._readError('unrecognized command status: ' + status)
      break
  }
  return status
}

// called when libpq is readable
Client.prototype._read = function () {
  var pq = this.pq
  // read waiting data from the socket
  // e.g. clear the pending 'select'
  if (!pq.consumeInput()) {
    // if consumeInput returns false
    // than a read error has been encountered
    return this._readError()
  }

  // check if there is still outstanding data
  // if so, wait for it all to come in
  if (pq.isBusy()) {
    return
  }

  // load our result object

  while (pq.getResult()) {
    const resultStatus = this._emitResult(this.pq)

    // if the command initiated copy mode we need to break out of the read loop
    // so a substream can begin to read copy data
    if (resultStatus === 'PGRES_COPY_BOTH' || resultStatus === 'PGRES_COPY_OUT') {
      break
    }

    // if reading multiple results, sometimes the following results might cause
    // a blocking read. in this scenario yield back off the reader until libpq is readable
    if (pq.isBusy()) {
      return
    }
  }

  this.emit('readyForQuery')

  var notice = this.pq.notifies()
  while (notice) {
    this.emit('notification', notice)
    notice = this.pq.notifies()
  }
}

// ensures the client is reading and
// everything is set up for async io
Client.prototype._startReading = function () {
  if (this._reading) return
  this._reading = true
  this.pq.on('readable', this._read)
  this.pq.startReader()
}

var throwIfError = function (pq) {
  var err = pq.resultErrorMessage() || pq.errorMessage()
  if (err) {
    throw new Error(err)
  }
}

Client.prototype._awaitResult = function (cb) {
  this._queryCallback = cb
  return this._startReading()
}

// wait for the writable socket to drain
Client.prototype._waitForDrain = function (pq, cb) {
  var res = pq.flush()
  // res of 0 is success
  if (res === 0) return cb()

  // res of -1 is failure
  if (res === -1) return cb(pq.errorMessage())

  // otherwise outgoing message didn't flush to socket
  // wait for it to flush and try again
  var self = this
  // you cannot read & write on a socket at the same time
  return pq.writable(function () {
    self._waitForDrain(pq, cb)
  })
}

// send an async query to libpq and wait for it to
// finish writing query text to the socket
Client.prototype._dispatchQuery = function (pq, fn, cb) {
  this._stopReading()
  var success = pq.setNonBlocking(true)
  if (!success) return cb(new Error('Unable to set non-blocking to true'))
  var sent = fn()
  if (!sent) return cb(new Error(pq.errorMessage() || 'Something went wrong dispatching the query'))
  this._waitForDrain(pq, cb)
}

Client.prototype._onResult = function (result) {
  if (this._resultCount === 0) {
    this._results = result
    this._rows = result.rows
  } else if (this._resultCount === 1) {
    this._results = [this._results, result]
    this._rows = [this._rows, result.rows]
  } else {
    this._results.push(result)
    this._rows.push(result.rows)
  }
  this._resultCount++
}

Client.prototype._onReadyForQuery = function () {
  // remove instance callback
  const cb = this._queryCallback
  this._queryCallback = undefined

  // remove instance query error
  const err = this._queryError
  this._queryError = undefined

  // remove instance rows
  const rows = this._rows
  this._rows = undefined

  // remove instance results
  const results = this._results
  this._results = undefined

  this._resultCount = 0

  if (cb) {
    cb(err, rows || [], results)
  }
}

function* yieldResults(pq, types) {
  const nfields = pq.nfields(), nrows = pq.ntuples(), table = {};
  for (let i=0; i<nrows; i++) {
    const row = [];
    for (let j=0; j<nfields; j++) {
      const func = types.getTypeParser(pq.ftype(j))
      const rawValue = pq.getvalue(i, j);
      if (rawValue === '' && pq.getisnull(i, j)) row.push(null);
      else row.push(func(rawValue));
    }
    yield row;
  }
}

function buildResult(pq, types, rowMode) {
  const nfields = pq.nfields(), nrows = pq.ntuples(), table = {};
  if (rowMode) {
    var i, j, row, func, rawValue;
    table.rows = [];
    table.columns = [];
    for (j=0; j<nfields; j++) table.columns.push(pq.fname(j));
    for (i=0; i<nrows; i++) {
      table.rows.push(row=[]);
      for (j=0; j<nfields; j++) {
        func = types.getTypeParser(pq.ftype(j))
        rawValue = pq.getvalue(i, j);
        if (rawValue === '' && pq.getisnull(i, j)) row.push(null);
        else row.push(func(rawValue));
      }
    }
    return table;
  }
  var i, j, col, func, rawValue;
  for (j=0; j<nfields; j++) {
    col = table[pq.fname(j)] = [];
    func = types.getTypeParser(pq.ftype(j))
    for (i=0; i<nrows; i++) {
      rawValue = pq.getvalue(i, j);
      if (rawValue === '' && pq.getisnull(i, j)) col.push(null);
      else col.push(func(rawValue));
    }
  }
  return table;
}
