import { NextResponse } from "next/server";

export async function GET() {
    try {
        const res = await fetch("http://localhost:8001/events?limit=20", {
            cache: "no-store",
        });
        const data = await res.json();
        return NextResponse.json(data);
    } catch (e) {
        return NextResponse.json({ error: String(e) }, { status: 500 });
    }
}
