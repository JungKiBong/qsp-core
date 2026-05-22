import * as zlib from 'zlib';

export interface QspFrameOptions {
  actor: string;
  targetObject: string;
  mutationFrom: string;
  mutationTo: string;
  resolves?: string[];
  state?: string;
  severity?: string;
  emotions?: Record<string, number>;
  meta?: string | null;
  timestamp?: number;
}

export class QspFrame {
  public actor: string;
  public targetObject: string;
  public mutationFrom: string;
  public mutationTo: string;
  public resolves: string[];
  public state: string;
  public severity: string;
  public emotions: Record<string, number>;
  public meta: string | null;
  public timestamp: number;

  constructor(options: QspFrameOptions) {
    this.actor = options.actor;
    this.targetObject = options.targetObject;
    this.mutationFrom = options.mutationFrom;
    this.mutationTo = options.mutationTo;
    this.resolves = options.resolves || [];
    this.state = options.state || 'success';
    this.severity = options.severity || 'medium';
    this.emotions = options.emotions || {};
    this.meta = options.meta || null;
    this.timestamp = options.timestamp || Math.floor(Date.now() / 1000);
  }

  /**
   * Converts the QspFrame into a High-Density Domain-Specific Language (HD-DSL) string.
   */
  public toHdDsl(): string {
    const resolvesStr = this.resolves.join(',');
    const mutationStr = `${this.targetObject}:${this.mutationFrom}->${this.mutationTo}`;

    const dslParts: string[] = [
      `ACT(${this.actor})`,
      `MUT(${mutationStr})`,
      `OBJ(${this.targetObject})`,
    ];

    if (this.resolves.length > 0) {
      dslParts.push(`RESOLVE(${resolvesStr})`);
    }

    dslParts.push(`STATE(${this.state})`, `SEV(${this.severity})`);

    if (Object.keys(this.emotions).length > 0) {
      const emoStr = Object.entries(this.emotions)
        .map(([k, v]) => `${k}:${v}`)
        .join(',');
      dslParts.push(`AFF(${emoStr})`);
    }

    if (this.meta) {
      const safeMeta = this.meta.replace(/\(/g, '[').replace(/\)/g, ']');
      dslParts.push(`META(${safeMeta})`);
    }

    dslParts.push(`TS(${this.timestamp})`);

    return dslParts.join('->');
  }

  /**
   * Parses a High-Density DSL string back into a structured QspFrame object.
   */
  public static fromHdDsl(dslStr: string): QspFrame {
    try {
      const matches: [string, string][] = [];
      const regex = /([A-Z]+)\((.*?)\)(?:->|$)/g;
      let match;
      while ((match = regex.exec(dslStr)) !== null) {
        matches.push([match[1], match[2]]);
      }

      const data = Object.fromEntries(matches);

      const actor = data['ACT'] || 'unknown';
      const obj = data['OBJ'] || 'unknown';

      const mutVal = data['MUT'] || '';
      let mutationFrom = 'unknown';
      let mutationTo = 'unknown';

      if (mutVal.includes(':') && mutVal.includes('->')) {
        const [, transition] = mutVal.split(':');
        const [mFrom, mTo] = transition.split('->');
        mutationFrom = mFrom.trim();
        mutationTo = mTo.trim();
      }

      const resolves = data['RESOLVE'] ? data['RESOLVE'].split(',').map((r) => r.trim()).filter(Boolean) : [];
      const state = data['STATE'] || 'success';
      const severity = data['SEV'] || 'medium';

      const emotions: Record<string, number> = {};
      if (data['AFF']) {
        const affVal = data['AFF'];
        for (const item of affVal.split(',')) {
          if (item.includes(':')) {
            const [k, v] = item.split(':');
            const parsedVal = parseFloat(v.trim());
            if (!isNaN(parsedVal)) {
              emotions[k.trim()] = parsedVal;
            }
          }
        }
      }

      let meta = data['META'] || null;
      if (meta) {
        meta = meta.replace(/\[/g, '(').replace(/\]/g, ')');
      }

      const timestamp = data['TS'] ? parseInt(data['TS'], 10) : Math.floor(Date.now() / 1000);

      return new QspFrame({
        actor,
        targetObject: obj,
        mutationFrom,
        mutationTo,
        resolves,
        state,
        severity,
        emotions,
        meta,
        timestamp,
      });
    } catch (e) {
      throw new Error(`Failed to parse HD-DSL: ${(e as Error).message}`);
    }
  }

  /**
   * Serializes the frame into Binary Episodic Frame (BEF) format using zlib compression.
   */
  public toBef(): Buffer {
    const compactDict = {
      a: this.actor,
      m: [this.targetObject, this.mutationFrom, this.mutationTo],
      r: this.resolves,
      s: this.state === 'success' ? 1 : this.state === 'failure' ? 0 : 2,
      v: this.severity === 'low' ? 0 : this.severity === 'medium' ? 1 : 2,
      e: this.emotions,
      d: this.meta,
      t: this.timestamp,
    };

    const compactJson = JSON.stringify(compactDict);
    return zlib.deflateSync(Buffer.from(compactJson, 'utf-8'));
  }

  /**
   * Deserializes a Binary Episodic Frame (BEF) back into a QspFrame object.
   */
  public static fromBef(binaryData: Buffer): QspFrame {
    const decompressed = zlib.inflateSync(binaryData).toString('utf-8');
    const compactDict = JSON.parse(decompressed);

    const actor = compactDict.a;
    const [obj, mFrom, mTo] = compactDict.m;
    const resolves = compactDict.r;

    const stateVal = compactDict.s;
    const state = stateVal === 1 ? 'success' : stateVal === 0 ? 'failure' : 'active';

    const sevVal = compactDict.v;
    const severity = sevVal === 0 ? 'low' : sevVal === 1 ? 'medium' : 'critical';

    const emotions = compactDict.e || {};
    const meta = compactDict.d || null;
    const timestamp = compactDict.t;

    return new QspFrame({
      actor,
      targetObject: obj,
      mutationFrom: mFrom,
      mutationTo: mTo,
      resolves,
      state,
      severity,
      emotions,
      meta,
      timestamp,
    });
  }
}

export class QspParser {
  public static encode(options: QspFrameOptions): QspFrame {
    return new QspFrame(options);
  }

  public static parseDsl(dslStr: string): QspFrame {
    return QspFrame.fromHdDsl(dslStr);
  }

  public static parseBef(binaryData: Buffer): QspFrame {
    return QspFrame.fromBef(binaryData);
  }
}
