import React from 'react';
import {
    Twitter,
    Mail,
    Link as LinkIcon,
    Printer,
    MoreHorizontal,
    Share2
} from 'lucide-react';

interface ArticleActionsProps {
    readTime: string;
}

export default function ArticleActions({ readTime }: ArticleActionsProps) {
    return (
        <div className="flex items-center justify-between border-t border-b border-gray-100 py-3 mb-10">
            <div className="flex items-center gap-6">
                <div className="flex items-center gap-2 text-xs font-bold text-gray-500 uppercase tracking-wider">
                    <Share2 size={16} />
                    Share
                </div>
                <div className="flex items-center gap-2">
                    <button className="w-8 h-8 rounded-full bg-gray-50 flex items-center justify-center text-gray-600 hover:bg-[#09365E] hover:text-white transition-all">
                        <Twitter size={14} fill="currentColor" />
                    </button>
                    <button className="w-8 h-8 rounded-full bg-gray-50 flex items-center justify-center text-gray-600 hover:bg-[#09365E] hover:text-white transition-all">
                        <Mail size={14} />
                    </button>
                    <button className="w-8 h-8 rounded-full bg-gray-50 flex items-center justify-center text-gray-600 hover:bg-[#09365E] hover:text-white transition-all">
                        <LinkIcon size={14} />
                    </button>
                    <button className="w-8 h-8 rounded-full bg-gray-50 flex items-center justify-center text-gray-600 hover:bg-[#09365E] hover:text-white transition-all">
                        <Printer size={14} />
                    </button>
                    <button className="w-8 h-8 rounded-full bg-gray-50 flex items-center justify-center text-gray-600 hover:bg-[#09365E] hover:text-white transition-all">
                        <MoreHorizontal size={14} />
                    </button>
                </div>
            </div>
            <div className="text-sm font-bold text-gray-500">
                {readTime} Read
            </div>
        </div>
    );
}
