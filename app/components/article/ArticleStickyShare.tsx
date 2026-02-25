import React from 'react';
import { Twitter, Mail, Link as LinkIcon, Printer, MoreHorizontal } from 'lucide-react';

export default function ArticleStickyShare() {
    return (
        <div className="hidden lg:flex flex-col items-center gap-4 sticky top-24 pt-2">
            <div className="flex flex-col items-center gap-1 mb-2">
                <div className="p-2 border border-gray-100 rounded-lg text-gray-400">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8" /><polyline points="16 6 12 2 8 6" /><line x1="12" y1="2" x2="12" y2="15" /></svg>
                </div>
                <span className="text-[10px] font-bold text-gray-400 uppercase tracking-tighter">Share</span>
            </div>

            <button className="p-3 text-gray-500 hover:text-[#09365E] transition-colors border-b border-gray-50 pb-4">
                <Twitter size={18} fill="currentColor" />
            </button>
            <button className="p-3 text-gray-500 hover:text-[#09365E] transition-colors border-b border-gray-50 pb-4">
                <Mail size={18} />
            </button>
            <button className="p-3 text-gray-500 hover:text-[#09365E] transition-colors border-b border-gray-50 pb-4">
                <LinkIcon size={18} />
            </button>
            <button className="p-3 text-gray-500 hover:text-[#09365E] transition-colors border-b border-gray-50 pb-4">
                <Printer size={18} />
            </button>
            <button className="p-3 text-gray-500 hover:text-[#09365E] transition-colors">
                <MoreHorizontal size={18} />
            </button>
        </div>
    );
}
